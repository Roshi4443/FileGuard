
import os

from audit.utils import log_activity
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.models import User

from .models import Document, DocumentPermission
from .forms import DocumentUploadForm, DocumentShareForm


@login_required
def document_list(request):
    owned_documents = Document.objects.filter(
        owner=request.user
    ).order_by('-uploaded_at')

    shared_documents = Document.objects.filter(
        permissions__user=request.user
    ).exclude(
        owner=request.user
    ).distinct().order_by('-uploaded_at')

    return render(
        request,
        'documents/document_list.html',
        {
            'documents': owned_documents,
            'shared_documents': shared_documents
        }
    )


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()

            log_activity(
                actor=request.user,
                action='UPLOAD',
                document=document,
                details='Document uploaded successfully.'
            )

            messages.success(
                request,
                "Document uploaded successfully."
            )
            return redirect('document_list')

    else:
        form = DocumentUploadForm()

    return render(
        request,
        'documents/upload.html',
        {'form': form}
    )


@login_required
def download_document(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id
    )

    is_owner = document.owner_id == request.user.id

    has_read_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        permission__in=['READ', 'EDIT']
    ).exists()

    if not (is_owner or has_read_permission):
        return messages_permission_denied(request)

    extension = os.path.splitext(document.file.name)[1]

    log_activity(
        actor=request.user,
        action='DOWNLOAD',
        document=document,
        details='Document downloaded successfully.'
    )

    return FileResponse(
        document.file.open('rb'),
        as_attachment=True,
        filename=f"{document.title}{extension}"
    )


@login_required
def edit_document(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id
    )

    is_owner = document.owner_id == request.user.id

    edit_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        permission='EDIT'
    ).exists()

    if not (is_owner or edit_permission):
        return messages_permission_denied(request)

    if request.method == 'POST':
        form = DocumentUploadForm(
            request.POST,
            request.FILES,
            instance=document
        )

        if form.is_valid():
            updated_document = form.save()

            log_activity(
                actor=request.user,
                action='EDIT',
                document=updated_document,
                details='Document title or file updated.'
            )

            messages.success(
                request,
                'Document updated successfully.'
            )

            return redirect('document_list')

    else:
        form = DocumentUploadForm(instance=document)

    return render(
        request,
        'documents/edit.html',
        {
            'form': form,
            'document': document
        }
    )


def messages_permission_denied(request):
    messages.error(
        request,
        "You do not have permission to access this document."
    )
    return redirect('document_list')


@login_required
def share_document(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = DocumentShareForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            permission = form.cleaned_data['permission']

            recipient = get_object_or_404(
                User,
                username=username
            )

            if recipient == request.user:
                form.add_error(
                    'username',
                    "You cannot share a document with yourself."
                )

            else:
                permission_record, created = (
                    DocumentPermission.objects.update_or_create(
                        document=document,
                        user=recipient,
                        defaults={
                            'permission': permission,
                            'granted_by': request.user
                        }
                    )
                )

                log_activity(
                    actor=request.user,
                    action='SHARE',
                    document=document,
                    target_user=recipient,
                    details=f'Document shared with permission: {permission}.'
                )

                messages.success(
                    request,
                    f"Document shared with {recipient.username}."
                )

                return redirect('document_list')

    else:
        form = DocumentShareForm()

    return render(
        request,
        'documents/share.html',
        {
            'form': form,
            'document': document
        }
    )


@login_required
def revoke_permission(request, document_id, permission_id):

    if request.method != 'POST':
        return redirect('document_list')

    document = get_object_or_404(
        Document,
        id=document_id,
        owner=request.user
    )

    permission = get_object_or_404(
        DocumentPermission,
        id=permission_id,
        document=document
    )

    recipient = permission.user

    log_activity(
        actor=request.user,
        action='REVOKE',
        document=document,
        target_user=recipient,
        details=f'Access revoked for {recipient.username}.'
    )

    permission.delete()

    messages.success(
        request,
        f"Access revoked for {recipient.username}."
    )

    return redirect('document_list')
