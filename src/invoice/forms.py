from django import forms
from django.core.validators import RegexValidator
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment, InvoiceForPaymentItem
from documents_сreating.models.reference import Currency, VatRate
from documents_сreating.models.organization import Organization, BankDetails, Status
from datetime import date
from django.forms import modelformset_factory

class InvoiceDocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


        organization_id = self.data.get('organization')
        if not organization_id:
            organization_id = self.initial.get('organization')
        buyer_id = self.data.get('buyer')
        if not buyer_id:
            buyer_id = self.initial.get('buyer')

        # Устанавливаем queryset для банков
        self.fields['organization_bank'].queryset = BankDetails.objects.filter(
            organization_id=organization_id
        ) if organization_id else BankDetails.objects.none()
        
        self.fields['buyer_bank'].queryset = BankDetails.objects.filter(
            organization_id=buyer_id
        ) if buyer_id else BankDetails.objects.none()

        # Фильтрация организаций для пользователя
        if self.request and hasattr(self.request, 'user'):
            user = self.request.user
            seller_status = Status.objects.filter(name="Seller").first()
            buyer_status = Status.objects.filter(name="Buyer").first()
            consignee_status = Status.objects.filter(name="Consignee").first()

            self.fields['organization'].queryset = Organization.objects.filter(
                status_org__status=seller_status,
                user=user
            ).distinct()
            
            self.fields['buyer'].queryset = Organization.objects.filter(
                status_org__status=buyer_status,
                user=user
            ).distinct()
            
            self.fields['consignee'].queryset = Organization.objects.filter(
                status_org__status=consignee_status,
                user=user
            ).distinct()

        # Обновление атрибутов полей
        for visible_field in self.visible_fields():
            if "from" not in visible_field.field.widget.attrs.get('class', ''):
                visible_field.field.widget.attrs.update({
                    'class': 'form-control',
                })

    currency = forms.ModelChoiceField(
        queryset=Currency.objects,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Нет',
        label='Валюта',
        required=False
    )

    vat_rate = forms.ModelChoiceField(
        queryset=VatRate.objects,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Нет',
        label='Ставка НДС',
        required=False
    )

    try:
        seller_status = Status.objects.filter(name="Seller").first()
    except:
        seller_status = None
    
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(status_org__status=seller_status).distinct(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новая организация',
        label='Организация',
        required=True
    )

    try:
        buyer_status = Status.objects.filter(name="Buyer").first()
    except:
        buyer_status = None

    buyer = forms.ModelChoiceField(
        queryset=Organization.objects.filter(status_org__status=buyer_status).distinct(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новый контрагент',
        label='Контрагент',
        required=True
    )
    try:
        consignee_status = Status.objects.filter(name="Consignee").first()
    except:
        consignee_status = None

    consignee = forms.ModelChoiceField(
        queryset=Organization.objects.filter(status_org__status=consignee_status).distinct(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новый Грузополучатель',
        label='Грузополучатель',
        required=True
    )

    organization_bank = forms.ModelChoiceField(
        queryset=BankDetails.objects,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новый банк',
        label='Банк организации',
        required=True
    )

    buyer_bank = forms.ModelChoiceField(
        queryset=BankDetails.objects,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новый банк',
        label='Банк покупателя',
        required=True
    )

    is_stamp = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Добавить печать и подпись'
    )

    class Meta:
        model = DocumentInvoiceForPayment
        fields = '__all__'
        exclude = ['user',]
        
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control w-md-25', 'value': date.today().strftime('%Y-%m-%d')}),
            'invoice_for_payment_data': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control w-md-25', 'value': date.today().strftime('%Y-%m-%d')}),
            'organization_telephone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона', 'inputmode': 'tel',
                       'type': 'tel'}),
            'organization_fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер факса'}),
            'customer_telephone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона', 'inputmode': 'tel',
                       'type': 'tel'}),
            'is_stamp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class InvoiceDocumentTableForm(forms.ModelForm):
    class Meta:
        model = InvoiceForPaymentItem
        fields = [
            'name',
            'quantity',
            'unit',
            'price',
            'sum',
        ]
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', "style": "height: 90px"}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'sum': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

InvoiceDocumentTableFormSet = modelformset_factory(
    InvoiceForPaymentItem,
    form=InvoiceDocumentTableForm,
    extra=1,
    max_num=1
)
