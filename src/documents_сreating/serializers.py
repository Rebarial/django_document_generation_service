from rest_framework import fields, serializers
from .models import (
    Organization, VatRate, Currency, DocumentType, SellerStatus,
    DocumentUPD, PaymentDocument, ShipmentDocument, DocumentItem
    )

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class DocumentUPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUPD
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

class DocumentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentItem
        fields = '__all__'


class PaymentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDocument
        fields = '__all__'

class ShipmentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDocument
        fields = '__all__'

class DocumentUPDSerializer(serializers.ModelSerializer):
    payment_docs = PaymentDocumentSerializer(many=True, required=False)
    shipment_docs = ShipmentDocumentSerializer(many=True, required=False)
    items_docs = DocumentItemSerializer(many=True, required=False)
    class Meta:
        model = DocumentUPD
        fields = '__all__'

