from django.contrib import admin
from .models import (
    Organization, DocumentUTD, UTDItem, VatRate, 
    Currency, DocumentType, SellerStatus,
    DocumentInvoiceForPayment, InvoiceForPaymentItem,
    BankDetails, Status,
    StatusOrganization,
)


class UTDItemInline(admin.TabularInline):
    model = UTDItem
    extra = 0
    fields = ('code', 'name', 'quantity', 'price', 'sum')

@admin.register(DocumentUTD)
class DocumentUTDAdmin(admin.ModelAdmin):
    inlines = [UTDItemInline]
    list_display = ('number', 'date', 'seller', 'buyer')
    list_filter = ('number','date', 'seller', 'buyer')
    search_fields = ('number', 'seller', 'buyer')
    date_hierarchy = 'date'

class InvoiceForPaymentItemInLine(admin.TabularInline):
    model = InvoiceForPaymentItem
    extra = 0
    fields = ("name", "quantity", "unit", "price", "sum")


@admin.register(DocumentInvoiceForPayment)
class DocumentInvoiceForPayment(admin.ModelAdmin):
    inlines = [InvoiceForPaymentItemInLine]

class StatusOrganizationInline(admin.TabularInline):
    model = StatusOrganization
    extra = 0
    fields = ('organization', 'status')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'address')
    search_fields = ('name', 'inn', 'address')
    inlines = [
        StatusOrganizationInline,
    ]

#admin.site.register(Organization)
admin.site.register(VatRate)
admin.site.register(Currency)
admin.site.register(DocumentType)
admin.site.register(SellerStatus)
admin.site.register(Status)
admin.site.register(StatusOrganization)
admin.site.register(BankDetails)
"""
admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Consignee)
admin.site.register(Consignor)

"""