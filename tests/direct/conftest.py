import os
import sys
import tempfile

import pytest


def _patch_windows_message_injection():
    """Work around gltest 0.29.2 unlinking an open stdin handle on Windows.

    ``gltest`` replaces fd 0 with a temporary file and immediately unlinks the
    path. POSIX permits that, but Windows rejects it while fd 0 is still open.
    Keep the file name on Windows; the OS cleans these short-lived test files
    when the process exits. The injected calldata and VM semantics are
    unchanged.
    """
    if os.name != "nt":
        return

    try:
        from gltest.direct import loader
    except ImportError:
        return

    def inject_message_to_fd0(vm):
        from genlayer.py import calldata
        from genlayer.py.types import Address
        from genlayer.py import storage
        from genlayer.py.storage.vec import DynArray
        from genlayer.py.storage._internal.core import InmemManager, ROOT_SLOT_ID
        from genlayer.py.storage._internal.generate import Lit, _storage_build

        if not getattr(storage.inmem_allocate, "_sourceroot_windows_patch", False):
            original_allocate = storage.inmem_allocate

            def allocate(t, *args, **kwargs):
                # genlayer-test 0.29.2 invokes GenericAlias.__init__ for a
                # DynArray[T], although the SDK's own storage descriptor has
                # already created the correct view. Skip that invalid init.
                if getattr(t, "__origin__", None) is DynArray:
                    td = _storage_build(t, {})
                    assert not isinstance(td, Lit)
                    return td.get(InmemManager().get_store_slot(ROOT_SLOT_ID), 0)
                return original_allocate(t, *args, **kwargs)

            allocate._sourceroot_windows_patch = True
            storage.inmem_allocate = allocate

        sender_addr = vm.sender
        if isinstance(sender_addr, bytes):
            sender_addr = Address(sender_addr)
        contract_addr = vm._contract_address
        if isinstance(contract_addr, bytes):
            contract_addr = Address(contract_addr)
        origin_addr = vm.origin
        if isinstance(origin_addr, bytes):
            origin_addr = Address(origin_addr)

        message_data = {
            "contract_address": contract_addr,
            "sender_address": sender_addr,
            "origin_address": origin_addr,
            "stack": [],
            "value": vm._value,
            "datetime": vm._datetime,
            "is_init": False,
            "chain_id": vm._chain_id,
            "entry_kind": 0,
            "entry_data": b"",
            "entry_stage_data": None,
        }
        fd, path = tempfile.mkstemp()
        try:
            os.write(fd, calldata.encode(message_data))
            os.lseek(fd, 0, os.SEEK_SET)
            vm._original_stdin_fd = os.dup(0)
            os.dup2(fd, 0)
        finally:
            os.close(fd)
            # fd 0 owns the file on Windows; defer cleanup to the OS.
            if os.name != "nt":
                os.unlink(path)

    loader._inject_message_to_fd0 = inject_message_to_fd0


_patch_windows_message_injection()


@pytest.fixture(autouse=True)
def _enable_pickling_validation(direct_vm):
    direct_vm.check_pickling = True

    # gltest 0.29.x refreshes sender/value after warp but can leave the raw
    # datetime cache stale. SourceRoot hashes transaction timestamps into
    # receipts, so keep the harness message aligned with the public warp time.
    original_refresh = direct_vm._refresh_gl_message

    def refresh_with_datetime():
        original_refresh()
        import sys

        gl = sys.modules.get("genlayer.gl")
        if gl is not None and isinstance(getattr(gl, "message_raw", None), dict):
            gl.message_raw["datetime"] = direct_vm._datetime

    direct_vm._refresh_gl_message = refresh_with_datetime
    direct_vm._refresh_gl_message()
    yield
