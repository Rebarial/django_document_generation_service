from django.forms.widgets import CheckboxSelectMultiple
from django import forms
from documents_сreating.models.organization import Organization, BankDetails, Status, StatusOrganization

class OrganizationForm(forms.ModelForm):

    statuses = forms.ModelMultipleChoiceField(
        queryset=Status.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Статусы'
    )

    IS_IP_CHOICES = (
        ('False', 'ОГРН'),
        ('True', 'ОГРНИП')
    )
    
    is_ip = forms.ChoiceField(
        choices=IS_IP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),  # используем стандартный select bootstrap
        label='Тип регистрации'
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
            'signature',
            'stamp',
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

