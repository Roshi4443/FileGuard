
from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),

    path('upload/', views.upload_document, name='upload_document'),

    path(
        'download/<int:document_id>/',
        views.download_document,
        name='download_document'
    ),

    path(
        'edit/<int:document_id>/',
        views.edit_document,
        name='edit_document'
    ),

    path(
        'share/<int:document_id>/',
        views.share_document,
        name='share_document'
    ),

    path(
        'revoke/<int:document_id>/<int:permission_id>/',
        views.revoke_permission,
        name='revoke_permission'
    ),
]
