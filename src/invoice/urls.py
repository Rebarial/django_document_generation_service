from django.urls import path
from .views import main, InvoiceDocumentCreateView, add_organization, add_bank_organization
from users.views import find_bank_by_bik, find_company_by_inn

urlpatterns = [
    path('', main, name='main'),
    path('invoice/', InvoiceDocumentCreateView.as_view(), name='invoice'),
    path('add-organization/', add_organization, name='add_organization'),
    path('add-bank-organization/', add_bank_organization, name='add_bank_organization'),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bik, name="find-bank"),
]