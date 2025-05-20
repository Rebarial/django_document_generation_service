from django.urls import path
from .views import main, InvoiceDocumentCreateView, add_organization, add_bank_organization, invoice_document, download_pdf
from users.views import find_bank_by_bik, find_company_by_inn

urlpatterns = [
    path('', main, name='main'),
    path('invoice/', InvoiceDocumentCreateView.as_view(), name='invoice'),
    path('invoice/<int:id_doc>', InvoiceDocumentCreateView.as_view(), name='invoice_edit'),
    path('download_document/<int:id_doc>', download_pdf, name='download_document'),
    path('add-organization/', add_organization, name='add_organization'),
    path('add-bank-organization/', add_bank_organization, name='add_bank_organization'),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bik, name="find-bank"),
    path('invoice_document/', invoice_document, name='invoice_document'),
]