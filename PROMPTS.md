# FileGuard – AI Prompt Usage Log

This document records AI prompts and assistance used during the development of FileGuard – Secure Document Sharing and Access Control System.

## Entry 01 – Project Architecture and Technology Selection

### Prompt Summary
Help design a secure document-sharing and access-control application for the Snovasys Fresher Hiring Challenge 2026.

### AI Assistance
- Selected Python and Django for backend development.
- Planned SQLite for database management.
- Designed separate applications for accounts, documents and audit.
- Planned private document storage and permission-based access.

### Developer Review
Reviewed the proposed architecture and selected Django for implementation.

### Verification Status
Django project and three applications created successfully.

---

## Entry 02 – Django Project Configuration

### Prompt Summary
Guide the setup of a Django project with separate applications for user authentication, document management and audit logging.

### AI Assistance
- Configured Django applications.
- Configured templates directory.
- Set project timezone to Asia/Kolkata.
- Configured authentication redirects.
- Created URL configurations.

### Developer Review
Reviewed project settings and tested the development server.

### Verification Status
Initial database migrations completed successfully.

---

## Entry 03 – User Authentication System

### Prompt Summary
Implement user registration, login, logout and a protected dashboard using Django authentication.

### AI Assistance
- Created registration form.
- Implemented registration and login views.
- Added logout functionality.
- Protected dashboard using login authentication.
- Created registration, login and dashboard templates.

### Developer Review
Tested registration, login, logout and unauthorized dashboard access.

### Verification Status
All authentication tests passed.

---

## Entry 04 – Document Database Model and Private Storage

### Prompt Summary
Create a Django document model and configure separate private storage for uploaded documents.

### AI Assistance
- Created Document model.
- Added document ownership using a foreign key.
- Generated unique filenames for uploaded files.
- Created a custom private storage backend.
- Configured a separate private storage directory.

### Developer Review
Reviewed the document model and private storage configuration.

### Verification Status
Document database migration completed successfully.

---

## Entry 05 – Document Upload and Listing

### Prompt Summary
Implement document uploading and owner-specific document listing with file size and extension restrictions.

### AI Assistance
- Created document upload form.
- Added 10 MB file size restriction.
- Added allowed file extension validation.
- Implemented upload and listing views.
- Created document upload and listing templates.

### Developer Review
Uploaded a sample document and verified that it appeared in the document list.

### Verification Status
Document upload and listing tested successfully.

---

## Entry 06 – Protected Document Downloads

### Prompt Summary
Implement secure document downloads with ownership verification.

### AI Assistance
- Created protected download view.
- Added document ownership verification.
- Used Django FileResponse for downloading files.
- Configured download URL.
- Added Download button to document listing.

### Developer Review
Tested document downloading using the owner's account.

### Verification Status
Owner-only document download tested successfully.

---

## Entry 07 – Document Sharing and Access Permissions

### Prompt Summary
Implement

# Additional AI Prompt Documentation

## Prompt 8: Implement Document Permission Management

**Objective:** Implement role-based document sharing and access control.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Implement document-sharing functionality in Django. Allow document owners to share files with other registered users using READ and EDIT permissions. Only document owners should be allowed to grant or revoke permissions. Ensure that unauthorized users cannot access shared documents."

**AI Assistance:**
- Suggested the DocumentPermission model.
- Helped implement READ and EDIT permission choices.
- Assisted with permission-checking logic.
- Helped implement sharing and revocation views.

**Human Validation:**
- Reviewed the permission logic.
- Tested owner, authorized and unauthorized user access.
- Verified that revoked users could no longer download documents.

**Result:** Implemented document-level permission management.

---

## Prompt 9: Implement Document Activity Audit Logging

**Objective:** Record important document-related activities.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Design and implement an audit logging system in Django to record document activities such as uploads, downloads, sharing and permission revocation. Store the user, document, action and timestamp for each activity."

**AI Assistance:**
- Suggested the AuditLog model.
- Helped implement activity logging utilities.
- Assisted with integrating logging into document views.
- Helped configure audit log administration.

**Human Validation:**
- Reviewed audit log records.
- Tested different document operations.
- Verified that corresponding activities were recorded.

**Result:** Implemented document activity tracking and audit logging.

---

## Prompt 10: Implement Secure Private Document Storage

**Objective:** Prevent direct public access to uploaded documents.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Implement private document storage in Django using a custom FileSystemStorage class. Store uploaded documents outside the public media directory, prevent public URL generation, and serve documents only through authenticated views with permission checks."

**AI Assistance:**
- Suggested a custom private storage class.
- Helped configure PRIVATE_MEDIA_ROOT.
- Assisted with UUID-based upload paths.
- Helped integrate permission-checked document downloads.

**Human Validation:**
- Reviewed the storage configuration.
- Tested document downloads through Django views.
- Verified that public URL generation was blocked.

**Result:** Implemented private document storage with controlled document access.

---

## Prompt 11: Implement Document Upload Validation

**Objective:** Validate uploaded files before storing them.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Implement Django file upload validation. Restrict uploads to PDF, DOC, DOCX, TXT, JPG, JPEG and PNG files. Enforce a maximum file size of 10 MB, reject empty files and validate basic file signatures and content."

**AI Assistance:**
- Helped implement extension validation.
- Suggested file-size restrictions.
- Assisted with basic file signature validation.
- Helped validate DOCX and UTF-8 text files.

**Human Validation:**
- Tested valid text files.
- Tested unsupported extensions.
- Tested empty files and oversized files.
- Tested invalid PDF content.

**Result:** Implemented upload validation with a 10 MB file-size limit and basic content checks.

---

## Prompt 12: Implement Document Editing

**Objective:** Allow authorized users to update existing documents.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Implement a document editing feature in Django. Allow document owners and users with EDIT permission to update document titles and replace uploaded files. Deny editing access to READ-only and unauthorized users. Record editing activity in the audit log."

**AI Assistance:**
- Helped implement the edit_document view.
- Assisted with permission verification.
- Helped integrate the existing upload form.
- Added EDIT activity logging.

**Human Validation:**
- Tested document editing as the owner.
- Tested editing with EDIT permission.
- Verified that READ-only and unauthorized users were denied.
- Tested file replacement.

**Result:** Implemented permission-based document editing.

---

## Prompt 13: Implement Old File Cleanup

**Objective:** Prevent unused files from accumulating when documents are replaced.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Update the Django document editing functionality so that when a user replaces an existing document file, the previous file is deleted from private storage after the replacement is successfully saved. Do not delete the existing file when only the document title is updated."

**AI Assistance:**
- Suggested tracking the previous file name.
- Helped implement old-file deletion after successful replacement.
- Assisted with checking whether a replacement file was uploaded.

**Human Validation:**
- Replaced an existing document.
- Verified that the new content was saved.
- Checked that the previous file was deleted from storage.

**Result:** Implemented old-file cleanup after document replacement.

---

## Prompt 14: Generate Automated Document Security Tests

**Objective:** Verify document access control and application functionality.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Create Django automated tests for document security, sharing permissions, download authorization, upload validation, document editing and audit logging. Include tests for unauthorized access and file replacement."

**AI Assistance:**
- Helped structure Django TestCase classes.
- Suggested test scenarios for owners, editors and readers.
- Assisted with upload validation tests.
- Helped add a test for old-file deletion.

**Human Validation:**
- Executed the automated test suite.
- Reviewed individual test results.
- Fixed issues identified during testing.

**Result:** Successfully executed 20 document application tests.

---

## Prompt 15: Design FileGuard Landing Page

**Objective:** Create a professional homepage for FileGuard.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Design a modern, responsive landing page for FileGuard, a secure document-sharing and access-control application. Include a navigation bar, hero section, feature cards, workflow explanation, login and registration buttons, and a footer. Use HTML, CSS and Django templates."

**AI Assistance:**
- Generated the initial HTML structure.
- Suggested CSS styling and responsive layouts.
- Helped create feature descriptions.
- Assisted with Django template integration.

**Human Validation:**
- Reviewed the generated HTML and CSS.
- Tested the homepage in the browser.
- Verified the login and registration navigation.

**Result:** Successfully implemented the FileGuard landing page.

---

## Prompt 16: Integrate Homepage with Django URL Routing

**Objective:** Configure the landing page as the application's root URL.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Integrate the FileGuard homepage into the existing Django URL configuration without breaking account authentication, document routes or the admin panel."

**AI Assistance:**
- Suggested Django TemplateView for the homepage.
- Helped configure the root URL.
- Preserved existing account and document URL patterns.

**Human Validation:**
- Executed Django system checks.
- Opened the homepage in the browser.
- Verified existing login and registration routes.

**Result:** Configured the FileGuard landing page at the root URL.

---

## Prompt 17: Debug Private File URL Rendering

**Objective:** Fix an error occurring when opening the document editing page.

**AI Tool:** ChatGPT

**Prompt Summary:**

"Debug a Django NotImplementedError occurring on the document editing page. The custom private storage class prevents public URL generation, but Django's default ClearableFileInput attempts to generate a URL for the existing file. Fix the issue without weakening private document storage."

**AI Assistance:**
- Helped identify the ClearableFileInput behavior.
- Suggested using Django FileInput instead.
- Helped update the document upload form while retaining file validation.

**Human Validation:**
- Updated the form widget.
- Opened the document editing page.
- Verified that document editing and replacement worked without generating public URLs.

**Result:** Resolved the private document URL rendering error while preserving private storage restrictions.

---

## AI Usage and Human Responsibility

AI tools were used as development assistants for requirement analysis, implementation suggestions, debugging, documentation and test-case generation.

The developer reviewed, modified and tested the generated code before incorporating it into the project. AI-generated suggestions were not treated as automatically correct. Application behavior was validated through Django system checks, automated tests and browser-based testing.
