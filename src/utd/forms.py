from django import forms
from documents_сreating.models.documents.upd import DocumentUPD, UPDItem, ShipmentDocument, PaymentDocument 
from django.forms import modelformset_factory
from datetime import date


class UtdDocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentUPD
        fields = '__all__'