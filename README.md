# FileGuard – Secure Document Sharing and Access Control System

## Project Overview
FileGuard is a Django-based document management application designed to provide secure document storage, controlled sharing and permission-based access.

## Technology Stack
- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap

## Implemented Features
- User registration and authentication
- Protected user dashboard
- Document upload with a 10 MB size limit
- File extension filtering
- Private document storage backend
- Owner-specific document listing
- Owner-only protected document downloads

## Django Applications
- `accounts` – User registration, login and authentication
- `documents` – Document storage, upload and access management
- `audit` – Planned activity logging

## Security Approach
- Authentication required for document operations
- Documents stored separately from public static files
- Download requests verify document ownership
- File upload size and extension restrictions

## Current Development Status
Document upload, listing and owner-only downloads are implemented and tested locally.

Document sharing, granular permissions, access revocation, audit logging, additional security testing and deployment are still in progress.

## Running Locally

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser and navigate to `/login/` or `/register/`.

## Project Status
Under active development for the Snovasys Fresher Hiring Challenge 2026.
