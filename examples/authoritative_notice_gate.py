# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


@gl.contract_interface
class ISourceRoot:
    class View:
        def is_authoritative(
            self,
            entity_id: u256,
            source_id: u256,
            required_scope_mask: u64,
            expected_entity_hash: str,
            expected_certificate_hash: str,
        ) -> bool: ...
        def authority_certificate(self, source_id: u256) -> str: ...

    class Write:
        pass


class AuthoritativeNoticeGate(gl.Contract):
    sourceroot: Address
    accepted: TreeMap[u256, str]

    def __init__(self, sourceroot: Address):
        self.sourceroot = sourceroot

    @gl.public.write
    def accept_notice(
        self,
        notice_id: u256,
        entity_id: u256,
        source_id: u256,
        required_scope_mask: u64,
        expected_entity_hash: str,
        expected_certificate_hash: str,
    ) -> None:
        if self.accepted.get(notice_id, "") != "":
            raise gl.vm.UserError("EXPECTED: notice already accepted")

        root = ISourceRoot(self.sourceroot)
        allowed = root.view().is_authoritative(
            entity_id,
            source_id,
            required_scope_mask,
            expected_entity_hash,
            expected_certificate_hash,
        )
        if not allowed:
            raise gl.vm.UserError("EXPECTED: source authority requirement not satisfied")

        certificate = root.view().authority_certificate(source_id)
        if certificate == "":
            raise gl.vm.UserError("EXPECTED: authority certificate unavailable")
        self.accepted[notice_id] = certificate

    @gl.public.view
    def get_notice_certificate(self, notice_id: u256) -> str:
        return self.accepted.get(notice_id, "")
