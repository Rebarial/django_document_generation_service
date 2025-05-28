from django import forms
from documents_сreating.models import DocumentUTD, UTDItem, Organization, VatRate, Currency, Status
from django.forms import modelformset_factory
from datetime import date
from documents_сreating.widgets import OrganizationWidget, PaymentDocumentWidget


class UtdDocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        print('REQUEST', self.request)

        # Фильтрация организаций для пользователя
        if self.request and hasattr(self.request, 'user'):
            user = self.request.user
            seller_status = Status.objects.filter(name="Seller").first() or None
            buyer_status = Status.objects.filter(name="Buyer").first() or None
            consignor_status = Status.objects.filter(name="Consignor").first() or None
            consignee_status = Status.objects.filter(name="Consignee").first() or None
            document_seller = Status.objects.filter(name="Doc seller").first() or None
            document_buyer = Status.objects.filter(name="Doc buyer").first() or None

            self.fields['seller'].queryset = Organization.objects.filter(
                status_org__status=seller_status,
                user=user
            ).distinct()
            
            self.fields['buyer'].queryset = Organization.objects.filter(
                status_org__status=buyer_status,
                user=user
            ).distinct()
            
            self.fields['consignor'].queryset = Organization.objects.filter(
                status_org__status=consignor_status,
                user=user
            ).distinct()

            self.fields['consignee'].queryset = Organization.objects.filter(
                status_org__status=consignee_status,
                user=user
            ).distinct()
            
            self.fields['document_seller'].queryset = Organization.objects.filter(
                status_org__status=document_seller,
                user=user
            ).distinct()
            
            self.fields['document_buyer'].queryset = Organization.objects.filter(
                status_org__status=document_buyer,
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

    
    seller = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        widget=OrganizationWidget(attrs={
            'label': 'Организация',
            'button': 'Редактировать организацию',
            'prefix': 'seller',
            }),
        empty_label='Новая организация',
        label='Организация',
        required=True
    )

    buyer = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        widget=OrganizationWidget(attrs={
            'label': 'Контрагент',
            'button': 'Редактировать контрагента',
            'prefix': 'buyer',
            }),
        empty_label='Новый контрагент',
        label='Контрагент',
        required=True
    )

    consignor = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        widget=OrganizationWidget(attrs={
            'label': 'Грузоотправитель',
            'button': 'Редактировать грузополучателя',
            'prefix': 'consignor',
            }),
        empty_label='Новый грузоотправитель',
        label='Грузоотправитель',
        required=True
    )

    consignee = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        widget=OrganizationWidget(attrs={
            'label': 'Грузополучатель',
            'button': 'Редактировать грузополучателя',
            'prefix': 'consignee',
            }),
        empty_label='Новый грузополучатель',
        label='Грузополучатель',  
        required=True
    )
    document_seller = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        widget=OrganizationWidget(attrs={
            'label': 'Продавец, составитель документа',
            'button': 'Редактировать составителя',
            'prefix': 'document_seller'
            }),
        empty_label='Новый продавец составитель',
        label='Продавец составитель',
        required=True
    )
    document_buyer = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        widget=OrganizationWidget(attrs={
            'label': 'Покупатель, составитель документа',
            'button': 'Редактировать составителя',
            'prefix': 'document_buyer',
            }),
        empty_label='Новый покупатель составитель',
        label='Покупатель составитель',
        required=True
    )

    is_stamp = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Добавить печать и подпись'
    )

    class Meta:
        model = DocumentUTD
        fields = '__all__'
        exclude = ['user',]
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control w-md-25', 'value': date.today().strftime('%Y-%m-%d')}),
            'corr_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control w-md-25', 'value': date.today().strftime('%Y-%m-%d')}),
            'transfer_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control w-md-25', 'value': date.today().strftime('%Y-%m-%d')}),
            'receipt_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control w-md-25', 'value': date.today().strftime('%Y-%m-%d')}),
            'shipping_document': forms.TextInput(
                attrs={'class': 'form-control w-md-50'}),
            'state_ID_contract': forms.TextInput(
                attrs={'class': 'form-control w-md-50'}),
            'basis_for_transfer': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'data_transportation': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'name': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'payment_document': PaymentDocumentWidget(),
        }
        labels = {
            'name': 'УПД №',
            'date': 'Дата создания документа',
            'organization': 'Организация',
            'shipper': 'Грузоотправитель',
            'counterparty': 'Контрагент',
            'consignee': 'Грузополучатель',
            'shipping_document': 'Документ об отгрузке',
            'state_ID_contract': 'Идентификатор гос. контракта',
            'basis_for_transfer': 'Основание передачи',
            'data_transportation': 'Данные о транспортировке и грузе',
            'shipment_date': 'Дата отгрузки',
            'date_of_receipt': 'Дата получения',
        }


class UtdDocumentTableForm(forms.ModelForm):
    class Meta:
        model = UTDItem
        fields = [
            'name',
            'code',
            'type_code',
            'unit',
            'excise',
            'quantity',
            'price',
            'sum',
            'country',
            'gtd_number',
        ]
        widgets = {
            'name': forms.Textarea(
                attrs={'class': 'form-control', 'required': 'required', "style": "height: 90px"}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'type_code': forms.TextInput(attrs={'class': 'form-control'}),
            'excise': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'gtd_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'sum': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


UtdDocumentTableFormSet = modelformset_factory(
    UTDItem,
    form=UtdDocumentTableForm,
    extra=1,
    max_num=1
)
