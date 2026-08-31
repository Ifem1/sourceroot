import os
import sys
import tempfile

import pytest


def _patch_message_injection():
    """Provide v0.3-compatible message injection for gltest 0.29.2.

    The pinned suite's compatibility loader can fail to resolve the v0.3 SDK
    modules before injecting stdin. GenVM decodes fd 0 at import time, so use
    the v0.3 module paths directly and install the message before loading the
    contract. Keep the file name on Windows because the OS rejects unlinking
    an open stdin handle; POSIX removes it immediately as usual.
    """
    try:
        from gltest.direct import loader
        from gltest.direct import sdk_compat
    except ImportError:
        return

    # The pinned v0.3 suite's compatibility helper expects a top-level
    # ``genlayer.types`` module, while this SDK artifact exposes it under
    # ``genlayer.py.types``.
    def import_types_compat():
        from genlayer.py import types as sdk_types

        return sdk_types

    sdk_compat.import_types = import_types_compat

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

        if not getattr(loader._allocate_contract, "_sourceroot_v03_patch", False):
            original_allocate_contract = loader._allocate_contract

            def allocate_contract(contract_cls, vm, *args, **kwargs):
                # The pinned testing-suite commit imports genlayer.storage,
                # while the v0.3 runner exposes this module as
                # genlayer.py.storage. Use the same descriptor-backed
                # allocation path with the VM's actual storage manager.
                try:
                    from genlayer.py.storage._internal.generate import (
                        ORIGINAL_INIT_ATTR,
                        _storage_build,
                    )

                    td = _storage_build(contract_cls, {})
                    slot = vm._storage.get_store_slot(storage.ROOT_SLOT_ID)
                    instance = td.get(slot, 0)
                    init = getattr(td, "cls", None)
                    if init is None:
                        init = getattr(contract_cls, "__init__", None)
                    else:
                        init = getattr(init, "__init__", None)
                    if init is not None:
                        if hasattr(init, ORIGINAL_INIT_ATTR):
                            init = getattr(init, ORIGINAL_INIT_ATTR)
                        init(instance, *args, **kwargs)
                    return instance
                except ImportError:
                    return original_allocate_contract(contract_cls, vm, *args, **kwargs)

            allocate_contract._sourceroot_v03_patch = True
            loader._allocate_contract = allocate_contract

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
            # Import only after fd 0 contains the encoded message. The v0.3
            # GenVM globals decode stdin during import.
            import genlayer.gl.genvm_contracts as genvm_contracts

            # The pinned runner keeps its module-level single-contract
            # sentinel between loader invocations, unlike the older runner.
            genvm_contracts.__known_contract__ = None

            # The v0.3 runner cannot import its legacy ``genlayer.vm`` alias
            # while applying the direct-mode run_nondet patch. Install the
            # equivalent patch once the SDK module is available.
            try:
                import genlayer.gl.vm as gl_vm
                from genlayer.py.types import Lazy

                sys.modules.setdefault("genlayer.vm", gl_vm)

                def direct_run_nondet(leader_fn, validator_fn, /, **kwargs):
                    from gltest.direct import wasi_mock

                    active_vm = wasi_mock.get_vm()
                    if active_vm._check_pickling:
                        loader._validate_pickling(leader_fn, "leader_fn")
                        loader._validate_pickling(validator_fn, "validator_fn")
                    active_vm._in_nondet = True
                    try:
                        result = leader_fn()
                    finally:
                        active_vm._in_nondet = False
                    active_vm._captured_validators.append(
                        (result, leader_fn, validator_fn)
                    )
                    return result

                def lazy_direct_run_nondet(leader_fn, validator_fn, /, **kwargs):
                    return Lazy(
                        lambda: direct_run_nondet(leader_fn, validator_fn, **kwargs)
                    )

                direct_run_nondet.lazy = lazy_direct_run_nondet
                gl_vm.run_nondet = direct_run_nondet
            except ImportError:
                pass

        finally:
            os.close(fd)
            # fd 0 owns the file on Windows; defer cleanup to the OS.
            if os.name != "nt":
                os.unlink(path)

    loader._inject_message_to_fd0 = inject_message_to_fd0


_patch_message_injection()


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
