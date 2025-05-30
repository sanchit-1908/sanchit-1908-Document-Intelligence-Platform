from django.urls import path
from .views import DocumentUploadView, DocumentListView, DocumentDetailView, DocumentDeleteView, ChatView, DocumentContentView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:id>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:id>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
    path("chat/<int:document_id>/", ChatView.as_view(), name="chat"),
    path('documents/content/<int:document_id>/', DocumentContentView.as_view(), name='document-content'),

]
