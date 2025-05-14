from django.urls import path
from .views import main, InvoiceDocumentCreateView

urlpatterns = [
    path('', main, name='main'),
    path('invoice/', InvoiceDocumentCreateView.as_view(), name='invoice')
]