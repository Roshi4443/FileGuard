# FileGuard – Security Threat Model

## 1. Project Overview

FileGuard is a secure document-sharing platform built using Django. It provides user authentication, private document storage, access permissions, document sharing, access revocation, and audit logging.

## 2. Identified Security Threats and Mitigations

### Threat 1: Unauthorized Document Access
**Risk:** An unauthorized user may attempt to access another user's documents.

**Mitigation:**
- Login is required for document operations.
- Document ownership is checked before owner-only sharing operations.
- Download access is checked against ownership and document permissions.

### Threat 2: Unauthorized File Downloads
**Risk:** A user may attempt to download a document using a direct or previously saved URL.

**Mitigation:**
- Every download request checks the user's current permission.
- Private files are stored outside publicly served media URLs.
- Revoked permissions no longer authorize downloads.

### Threat 3: Unauthorized Document Sharing
**Risk:** A user may attempt to share documents owned by someone else.

**Mitigation:**
- Only the document owner can access the sharing operation.
- Users cannot share documents with themselves.
- Recipient accounts are validated.

### Threat 4: Continued Access After Revocation
**Risk:** A recipient may retain access after the owner revokes permission.

**Mitigation:**
- Permission records are deleted when access is revoked.
- Download authorization checks the current database permission.
- Previously saved download links are rechecked on every request.

### Threat 5: Unsafe File Uploads
**Risk:** Attackers may upload unsupported or excessively large files.

**Mitigation:**
- File extensions are restricted to an allowed list.
- Upload size is limited to 10 MB.

**Remaining limitation:** Extension validation alone does not verify actual file content.

### Threat 6: Lack of Activity Visibility
**Risk:** Important document operations may go unrecorded.

**Mitigation:**
- Audit logs record uploads, downloads, sharing, and revocation.
- Records include the actor, document, target user when applicable, and timestamp.
- Audit records are read-only through the Django Admin interface.

## 3. Security Testing Performed

The following tests were performed manually:

1. Unauthorized document download was denied.
2. Shared document download was permitted.
3. Revoked document disappeared from the recipient's list.
4. Previously saved download URL was denied after revocation.
5. Upload activity was recorded.
6. Download activity was recorded.
7. Sharing activity was recorded.
8. Revocation activity was recorded.

## 4. Known Limitations and Future Improvements

- Validate actual file content, not only extensions.
- Add automated security tests.
- Implement meaningful EDIT permission functionality.
- Add stronger audit-log integrity protections.
- Configure production-grade deployment settings.
- Add rate limiting and upload security controls.

## 5. Conclusion

FileGuard implements basic document access control and audit logging. Manual tests confirmed the core upload, download, sharing, and revocation workflows. Further security testing and production hardening are required before real-world deployment.
