# FileGuard – Secure Document Sharing and Access Control System

## 1. Project Overview

FileGuard is a Django-based secure document-sharing application designed to provide controlled access to important documents.

It allows users to upload, store, share, download and edit documents with permission-based access control.

The application supports two permission levels: READ and EDIT. Document owners can manage sharing permissions, revoke access and monitor document-related activities through audit logs.

The main objective of FileGuard is to provide a centralized document management platform where access is controlled and important activities are recorded.

## 2. Problem Statement

Traditional document-sharing methods can make it difficult to control who can access, modify or download shared files.

Common challenges include:

- Unauthorized document access.
- Lack of permission-based sharing.
- Difficulty managing shared document access.
- Limited visibility into document activities.
- Unnecessary accumulation of replaced files.

FileGuard addresses these challenges through document-level permissions, private file storage, upload validation and activity auditing.

## 3. Key Features

### User Authentication
- User registration and login.
- Authenticated access to protected pages.
- Individual user accounts.

### Document Management
- Upload and manage documents.
- Download authorized documents.
- Update document titles.
- Replace existing document files.
- UUID-based file naming.

### Role-Based Access Control
- READ permission for viewing and downloading documents.
- EDIT permission for viewing, downloading and modifying documents.
- Document owners can share documents with registered users.
- Document owners can revoke permissions.
- Unauthorized users are prevented from accessing protected documents.

### Private Document Storage
- Custom Django file storage implementation.
- Documents stored outside the public media directory.
- Public URL generation disabled for private documents.
- Document downloads handled through permission-checked application views.

### File Upload Validation
- Allowed extensions: PDF, DOC, DOCX, TXT, JPG, JPEG and PNG.
- Maximum file size: 10 MB.
- Empty files are rejected.
- Basic file signature and content validation.

### Audit Logging
Records important document activities, including:

- Document uploads.
- Document downloads.
- Document sharing.
- Permission revocation.
- Document editing.

### File Replacement and Cleanup
- Authorized users can replace existing files.
- Previous files are deleted from private storage after successful replacement.
- Updating only a document title does not require replacing the file.

### Landing Page
- Responsive homepage.
- Project introduction and feature overview.
- Login and registration navigation.
- Explanation of the document-sharing workflow.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python |
| Web Framework | Django |
| Frontend | HTML, CSS |
| Database | SQLite |
| Authentication | Django Authentication |
| File Storage | Django FileSystemStorage |
| Testing | Django TestCase |
| Version Control | GitHub |
| Development Environment | Visual Studio Code |

## 5. System Architecture

FileGuard follows Django's Model-Template-View (MTV) architecture.

### Main Application Components

**Accounts**
- User registration.
- User login and authentication.
- Dashboard access.

**Documents**
- Document upload and download.
- Document editing.
- Permission management.
- Private file storage.
- File validation.

**Audit**
- Document activity records.
- Audit log administration.
- Activity tracking.

### Document Access Workflow

1. A registered user uploads a document.
2. The document is associated with its owner.
3. The owner shares the document with another registered user.
4. The owner assigns READ or EDIT permission.
5. The application checks permissions when protected document operations are requested.
6. Important activities are recorded in the audit log.
7. The owner can revoke access when required.

## 6. Access Control Model

FileGuard implements document-level access control with three user categories.

### Document Owner
- Can upload documents.
- Can download documents.
- Can edit document titles and replace files.
- Can share documents with other registered users.
- Can revoke previously granted permissions.

### READ Permission
- Can view and download shared documents.
- Cannot edit or replace documents.
- Cannot share documents with other users.
- Cannot revoke permissions.

### EDIT Permission
- Can view and download shared documents.
- Can edit document titles.
- Can replace existing document files.
- Cannot share documents with other users.
- Cannot revoke permissions.

### Unauthorized Users
- Cannot download protected documents.
- Cannot edit documents.
- Cannot access protected document operations.

All permissions are checked on the backend for protected operations. Hiding buttons in the frontend is not treated as an authorization mechanism.

## 7. Project Structure

The main project structure is:

```text
FileGuard/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── urls.py
│   └── views.py
│
├── audit/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   └── models.py
│
├── documents/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── fileguard/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── home.html
│
├── .gitignore
├── manage.py
├── PROMPTS.md
├── THREATS.md
└── README.md
```

Note: The `private_storage/` directory is created locally when files are uploaded. It is excluded from GitHub to keep uploaded documents private.

## 8. Installation and Setup

Follow these steps to run FileGuard locally.

### Prerequisites

- Python 3.13 or a compatible version
- Django 6.1.3
- A code editor such as Visual Studio Code
- Git (optional, for cloning the repository)

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/FileGuard.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Open the project folder

```bash
cd FileGuard
```

### Step 3: Install Django

```bash
pip install Django==6.1.3
```

### Step 4: Apply database migrations

```bash
python manage.py migrate
```

### Step 5: Create an administrator account

```bash
python manage.py createsuperuser
```

### Step 6: Start the development server

```bash
python manage.py runserver
```

Open the following address in your browser:

```text
http://127.0.0.1:8000/
```

## 9. Automated Testing

FileGuard includes automated tests to verify important application features and security-related behaviour.

The tests cover:

- Document upload validation.
- Document access permissions.
- Owner and recipient access restrictions.
- Document download authorization.
- Permission sharing and revocation.
- Document editing and file replacement.
- Audit log creation.
- Deletion of old files after replacement.

Run the tests using:

```bash
python manage.py test documents -v 2
```

The project previously passed 20 automated tests. Run the command again after the latest code changes to confirm the current test results.

## 10. Security Considerations

FileGuard follows a security-focused approach to document management.

- Uploaded documents are stored in private storage rather than being exposed through public media URLs.
- Document downloads are handled through protected Django views.
- Access permissions are checked on the server before allowing document operations.
- Only document owners can share documents or revoke permissions.
- Permission revocation removes the recipient's access.
- File uploads have size, extension and basic content validation.
- Important document activities are recorded in audit logs.
- Audit records are protected from modification through the Django admin interface.
- Database files, private uploaded documents and environment files are excluded from Git tracking.

**Security limitations:**

This project is a prototype and has not undergone a professional security audit. It does not currently include antivirus scanning, advanced malware detection or enterprise-grade identity management. Additional hardening is required before production use.

## 11. AI-Assisted Development

AI tools were used as development assistants during the implementation of FileGuard.

They helped with:

- Understanding Django concepts and project structure.
- Planning document permission management.
- Implementing access-control checks.
- Developing file upload validation.
- Implementing audit logging.
- Debugging application errors.
- Writing and improving automated tests.
- Preparing security documentation.

All generated code and suggestions were reviewed, tested and adjusted during development.

Refer to `PROMPTS.md` for the AI prompt documentation.

## 12. Security Documentation

The repository includes `THREATS.md`, which documents the security considerations of FileGuard.

It covers:

- Assets that need protection.
- Potential security threats.
- Unauthorized document access.
- Permission management.
- File storage security.
- Access revocation.
- Audit logging.
- Security limitations and testing considerations.

## 13. Future Enhancements

Potential improvements for future versions include:

- Multi-factor authentication.
- Email notifications for document sharing.
- Document expiry and automatic access revocation.
- Advanced audit log monitoring.
- Antivirus and malware scanning.
- Cloud-based private object storage.
- More advanced role-based access control.
- Improved administrative security monitoring.

## 14. Conclusion

FileGuard demonstrates a secure document-sharing approach using Django, with private file storage, permission-based access control, document editing, access revocation and activity auditing.

The project focuses on protecting document confidentiality and ensuring that access is controlled by the document owner.

It provides a foundation for further development into a more advanced secure document management platform.
