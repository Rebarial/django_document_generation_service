from django.urls import path, include
from .api.create_document import DocumentUPDViewSet, DocumentInvoiceForPaymentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'upd', DocumentUPDViewSet)
router.register(r'invoiceforpayment', DocumentInvoiceForPaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]