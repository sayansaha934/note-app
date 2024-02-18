# urls.py
from django.urls import path
from .views import CreateNoteView, UpdateNoteView, GetNoteView, ShareNoteView, GetNoteVersionView

urlpatterns = [
    path('create', CreateNoteView.as_view(), name='create_note'),
    path('<uuid:pk>/update', UpdateNoteView.as_view(), name='update_note'),
    path('<uuid:pk>', GetNoteView.as_view(), name='get_note'),
    path('share', ShareNoteView.as_view(), name='share_note'),
    path('version-history/<uuid:note_id>/', GetNoteVersionView.as_view(), name='get_note_version'),

    # Add other URLs as needed
]
