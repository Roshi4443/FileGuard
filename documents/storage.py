from django.core.files.storage import FileSystemStorage
from django.conf import settings


class PrivateDocumentStorage(FileSystemStorage):

    def __init__(self, *args, **kwargs):
        kwargs["location"] = settings.PRIVATE_MEDIA_ROOT
        kwargs["base_url"] = None
        super().__init__(*args, **kwargs)

    def url(self, name):
        raise NotImplementedError(
            "Private documents cannot have public URLs."
        )