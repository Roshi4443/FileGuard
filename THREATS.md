# FileGuard - Security Threat Analysis

Documenting security risks, mitigation strategies
and testing results.

## Document Access Control

### Threat 1: Unauthorized Document Access

Risk:
A user may attempt to download another user's private document.

Mitigation:
- Require authentication.
- Verify document ownership or an explicit permission record.
- Check authorization on every download request.

Status: Implemented and tested.

### Threat 2: Unauthorized Document Sharing

Risk:
A user may attempt to share documents owned by another user.

Mitigation:
- Only document owners can access the sharing operation.
- Validate the recipient account.
- Store permissions separately for each document.

Status: Implemented.

### Threat 3: Continued Access After Revocation

Risk:
A recipient may attempt to download a document after their permission has been revoked.

Mitigation:
- Delete the corresponding permission record.
- Check the current database permission on every download request.

Status: Revocation view implemented; testing pending.
