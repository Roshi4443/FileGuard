
import os
import zipfile
from io import BytesIO

from django import forms
from django.contrib.auth.models import User

from .models import Document


class DocumentUploadForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['title', 'file']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document title'
            }),

            # FileInput avoids generating public URLs
            # for existing private documents.
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        max_size = 10 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                "File size must not exceed 10 MB."
            )

        if uploaded_file.size == 0:
            raise forms.ValidationError(
                "Empty files are not allowed."
            )

        extension = os.path.splitext(
            uploaded_file.name
        )[1].lower()

        allowed_extensions = [
            '.pdf', '.doc', '.docx',
            '.txt', '.jpg', '.jpeg', '.png'
        ]

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "This file type is not allowed."
            )

        uploaded_file.seek(0)
        header = uploaded_file.read(16)
        uploaded_file.seek(0)

        if extension == '.pdf':
            if not header.startswith(b'%PDF-'):
                raise forms.ValidationError(
                    "Invalid PDF file content."
                )

        elif extension in ['.jpg', '.jpeg']:
            if not header.startswith(b'\xff\xd8\xff'):
                raise forms.ValidationError(
                    "Invalid JPEG image content."
                )

        elif extension == '.png':
            if not header.startswith(b'\x89PNG\r\n\x1a\n'):
                raise forms.ValidationError(
                    "Invalid PNG image content."
                )

        elif extension == '.doc':
            if not header.startswith(
                b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
            ):
                raise forms.ValidationError(
                    "Invalid DOC file content."
                )

        elif extension == '.docx':
            try:
                uploaded_file.seek(0)

                with zipfile.ZipFile(
                    BytesIO(uploaded_file.read())
                ) as archive:

                    if 'word/document.xml' not in archive.namelist():
                        raise forms.ValidationError(
                            "Invalid DOCX document."
                        )

            except zipfile.BadZipFile:
                raise forms.ValidationError(
                    "Invalid DOCX file content."
                )

            finally:
                uploaded_file.seek(0)

        elif extension == '.txt':
            uploaded_file.seek(0)
            content = uploaded_file.read()

            if b'\x00' in content:
                raise forms.ValidationError(
                    "Invalid text file content."
                )

            try:
                content.decode('utf-8')

            except UnicodeDecodeError:
                raise forms.ValidationError(
                    "Text files must use UTF-8 encoding."
                )

            finally:
                uploaded_file.seek(0)

        return uploaded_file


class DocumentShareForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter recipient username'
        })
    )

    permission = forms.ChoiceField(
        choices=[
            ('READ', 'Read Only'),
            ('EDIT', 'Read and Edit')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username does not exist."
            )

        return username
