from django import forms
from django.core.validators import RegexValidator
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment, InvoiceForPaymentItem
from documents_сreating.models.reference import Currency, VatRate
from documents_сreating.models.organization import Organization, BankDetails, Status, StatusOrganization#, Seller, Buyer, Consignee, Consignor
from django.forms import inlineformset_factory
from django.forms import TextInput, DateInput, NumberInput
from django.forms.widgets import CheckboxSelectMultiple
from datetime import date
from django.forms import modelformset_factory

class InvoiceDocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        print(kwargs)

        if 'initial' in kwargs and 'organization' in kwargs['initial']:
            self.fields['organization_bank'].queryset = BankDetails.objects.filter(
                    organization=kwargs['initial']['organization']
                )
        elif 'data' in kwargs and 'organization' in kwargs['data']:
            self.fields['organization_bank'].queryset = BankDetails.objects.filter(
                    organization=kwargs['data']['organization']
                )
        else:
            self.fields['organization_bank'].queryset = BankDetails.objects.none()

        if 'initial' in kwargs and 'buyer' in kwargs['initial']:
            self.fields['buyer_bank'].queryset = BankDetails.objects.filter(
                    organization=kwargs['initial']['buyer']
                )
        elif 'data' in kwargs and 'buyer' in kwargs['data']:
            self.fields['buyer_bank'].queryset = BankDetails.objects.filter(
                    organization=kwargs['data']['buyer']
                )
        else:
            self.fields['buyer_bank'].queryset = BankDetails.objects.none()

        print(self.fields['organization_bank'].queryset)

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
        

        for visible_field in self.visible_fields():
            if ("from" not in visible_field.field.widget.attrs.get('class', '')):
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

    seller_status = Status.objects.filter(name="Seller").first()
    
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(status_org__status=seller_status).distinct(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новая организация',
        label='Организация',
        required=True
    )

    buyer_status = Status.objects.filter(name="Buyer").first()

    buyer = forms.ModelChoiceField(
        queryset=Organization.objects.filter(status_org__status=buyer_status).distinct(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Новый контрагент',
        label='Контрагент',
        required=True
    )

    consignee_status = Status.objects.filter(name="Consignee").first()
    
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

class OrganizationForm(forms.ModelForm):

    statuses = forms.ModelMultipleChoiceField(
        queryset=Status.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Статусы'
    )

    class Meta:
        model = Organization
        fields = [
            'name',
            'statuses', 
            'inn',
            'kpp',
            'is_ip',
            'ogrn',
            'address',
            'telephone',
            'fax',
            'director_position',
            'director_name',
            'accountant_name',
            'conventional_name',
            'stamp',
            'signature',
        ]
        exclude = ['user', 'full_name']

        widgets = {
            'statuses': forms.CheckboxSelectMultiple(attrs={
                                                        'class': 'form-check form-check-inline',
                                                    }),
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название организации'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название организации'}),
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ИНН', 'pattern': '[0-9]+',
                                          'title': 'ИНН может содержать только цифры'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите КПП', 'pattern': '[0-9]+',
                                          'title': 'КПП может содержать только цифры'}),
            'is_ip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+',
                                           'title': 'ОГРН может содержать только цифры', 'placeholder': 'ОГРН/ОГРНИП'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'list': 'address_list'}),
            'telephone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона', 'inputmode': 'tel',
                       'type': 'tel'}),
            'fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер факса'}),
            'director_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите должность руководителя'}),
            'director_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя руководителя'}),
            'accountant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя бухгалтера'}),
            'conventional_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите условное наимнование организации'}),
            'stamp': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'signature': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'stamp':
                field.label = ''
                field.help_text = 'Загрузите печать компании'
            elif name == 'signature':
                field.label = ''
                field.help_text = 'Загрузите подпись руководителя'
            else:
                field.help_text = ''


class BankDetailsOrganizationForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = '__all__'
        exclude = ['organization']

        widgets = {
            'bic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите БИК банка', 'pattern': '[0-9]+',
                                'title': 'БИК может содержать только цифры'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название банка'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'list': 'address_list_bank'}),
            'correspondent_account': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите кор.счет', 'pattern': '[0-9]+',
                       'title': 'Кор.счет может содержать только цифры'}),
            'current_account': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите расчетный счет', 'pattern': '[0-9]+',
                       'title': 'Расчетный счет может содержать только цифры'}),
        }

