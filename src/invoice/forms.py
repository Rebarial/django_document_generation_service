from django import forms
from django.core.validators import RegexValidator
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment, InvoiceForPaymentItem
from django.forms import inlineformset_factory
from django.forms import TextInput, DateInput, NumberInput

InvoiceItemFormSet = inlineformset_factory(
    DocumentInvoiceForPayment,
    InvoiceForPaymentItem,
    fields=('name', 'quantity', 'unit', 'price', 'sum'),
    extra=1,
    can_delete=True
)

class InvoiceDocumentForm(forms.ModelForm):
    # Валидаторы
    inn_validator = RegexValidator(r'^\d+$', 'ИНН должен содержать только цифры.')
    kpp_validator = RegexValidator(r'^\d+$', 'КПП должен содержать только цифры.')
    bik_validator = RegexValidator(r'^\d+$', 'БИК должен содержать только цифры.')
    
    # Переопределение полей для валидации
    organization_inn = forms.CharField(validators=[inn_validator], required=False)
    organization_kpp = forms.CharField(validators=[kpp_validator], required=False)
    organization_bik = forms.CharField(validators=[bik_validator], required=False)

    class Meta:
        model = DocumentInvoiceForPayment
        fields = '__all__'
        widgets = {
            # Даты
            'invoice_for_payment_data': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            # Числовые поля
            'quantity': NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'price': NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'sum': NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)