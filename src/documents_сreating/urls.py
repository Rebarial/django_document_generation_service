from django.urls import path, include
from .api.create_document import DocumentUTDViewSet, DocumentInvoiceForPaymentViewSet
from rest_framework import routers
from documents_сreating.views import (
    add_organization,
    add_bank_organization,
    main,
    download_pdf,
    find_bank_by_bic,
    find_company_by_inn,
    edit_organization,
    search_counterparty,
    inn_autocomplete,
    bank_autocomplete,
    add_counterparty_from_profile,
    add_organization_from_profile
    )


router = routers.DefaultRouter()
router.register(r"upd", DocumentUTDViewSet)
router.register(r"invoiceforpayment", DocumentInvoiceForPaymentViewSet)

urlpatterns = [
    path("", main, name="main"),
    path("download_document/<str:doc_name>/<int:doc_id>", download_pdf, name="download_document"),
    path("add-organization/", add_organization, name="add_organization"),
    path("add-bank-organization/", add_bank_organization, name="add_bank_organization"),
    path("", include(router.urls)),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bic, name="find-bank"),
    path('edit_organization/<int:id_org>', edit_organization, name='edit_organization'),
    path('api/search-counterparty/', search_counterparty, name='search_counterparty'),
    path('inn_autocomplete/', inn_autocomplete, name='inn_autocomplete'),
    path('bank_autocomplete/', bank_autocomplete, name='bank_autocomplete'),
    path('add-organization-profile/', add_organization_from_profile, name='add-organization-profile'),
    path('add-counterparty-profile/', add_counterparty_from_profile, name='add-counterparty-profile'),
]