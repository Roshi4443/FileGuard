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
