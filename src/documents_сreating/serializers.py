from rest_framework import fields, serializers
from .models import (
    Organization, VatRate, Currency, DocumentType, SellerStatus,
    DocumentUTD, UTDItem,
    DocumentInvoiceForPayment, InvoiceForPaymentItem
    )

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class DocumentUTDSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUTD
        fields = '__all__'

class VatRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatRate
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        
class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class SellerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerStatus
        fields = '__all__'

class UTDItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UTDItem 
        fields = '__all__'


class DocumentUTDSerializer(serializers.ModelSerializer):
    items_docs = UTDItemSerializer(many=True, required=False)
    class Meta:
        model = DocumentUTD
        fields = '__all__'

class InvoiceForPaymentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceForPaymentItem 
        fields = '__all__'

class DocumentInvoiceForPaymentSerializer(serializers.ModelSerializer):
    items_docs = InvoiceForPaymentItemSerializer(many=True, required=False)
    class Meta:
        model = DocumentInvoiceForPayment
        fields = '__all__'
