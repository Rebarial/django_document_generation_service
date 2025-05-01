from django.contrib import admin
from .models import (
    Organization, DocumentUPD, PaymentDocument, 
    ShipmentDocument, DocumentItem, VatRate, 
    Currency, DocumentType, SellerStatus
)

class PaymentDocumentInline(admin.TabularInline):
    model = PaymentDocument
    extra = 0
    fields = ('number', 'date')

class ShipmentDocumentInline(admin.TabularInline):
    model = ShipmentDocument
    extra = 0
    fields = ('name', 'number', 'date')

class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    extra = 0
    fields = ('code', 'name', 'quantity', 'price', 'amount')

@admin.register(DocumentUPD)
class DocumentUPDAdmin(admin.ModelAdmin):
    inlines = [PaymentDocumentInline, ShipmentDocumentInline, DocumentItemInline]
    list_display = ('invoice_number', 'invoice_date', 'seller_name', 'customer_name')
    list_filter = ('invoice_number','invoice_date', 'seller_name', 'customer_name')
    search_fields = ('invoice_number', 'seller_name', 'customer_name')
    date_hierarchy = 'invoice_date'

admin.site.register(Organization)
admin.site.register(VatRate)
admin.site.register(Currency)
admin.site.register(DocumentType)
admin.site.register(SellerStatus)
