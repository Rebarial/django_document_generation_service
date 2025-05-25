from django.urls import path
from .views import UtdDocumentCreateView, utd_document

urlpatterns = [
    path('', UtdDocumentCreateView.as_view(), name='utd'),
    path('<int:id_doc>', UtdDocumentCreateView.as_view(), name='utd_edit'),
    path('list', utd_document, name='utd_document'),
]