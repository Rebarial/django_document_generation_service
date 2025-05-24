from django.urls import path
from .views import InvoiceDocumentCreateView, invoice_document

urlpatterns = [
    path('', InvoiceDocumentCreateView.as_view(), name='invoice'),
    path('<int:id_doc>', InvoiceDocumentCreateView.as_view(), name='invoice_edit'),
    path('list', invoice_document, name='invoice_document'),
]