from django.db import models
from ..base import BaseModel
from ..reference import VatRate, Currency, DocumentType, SellerStatus
from .base import BaseDocument


class InvoiceForPaymentItem(BaseModel):
    document = models.ForeignKey('DocumentInvoiceForPayment', on_delete=models.CASCADE, related_name='items_docs', verbose_name='Документ')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Наименование')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Количество')
    unit = models.CharField(max_length=100, blank=True, null=True, verbose_name='Единица измерения')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Сумма')

    class Meta:
        verbose_name = 'Товар документа оплаты'
        verbose_name_plural = 'Товары документа оплаты'

class DocumentInvoiceForPayment(BaseDocument):

    invoice_for_payment_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер счет на оплату')
    invoice_for_payment_data = models.DateField(blank=True, null=True, verbose_name='Дата счет на оплату')

    #Информация о организации
    organization_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Организация Наименование')
    organization_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='Организация ИНН')
    organization_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='Организация КПП')
    organization_is_IP = models.BooleanField(default=False, verbose_name='организация является ИП')
    organization_main_state_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Основной государственный регистрационный номер')
    organization_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Адрес')
    organization_telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Организация Телефон')
    organization_fax = models.CharField(max_length=11, blank=True, null=True, verbose_name='Организация Факс')
    organization_director_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Должность директора')
    organization_director_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Директор')
    organization_accountant_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Бухгалтер')
    organization_conventional_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация условное наименование')

    #Банковские реквизиты организации
    organization_bik = models.CharField(max_length=9, blank=True, null=True, verbose_name='Организация БИК')
    organization_bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Наименование банка')
    organization_bank_place_of_registration = models.CharField(max_length=100, blank=True, null=True, verbose_name='Организация Место нахождения банка')
    organization_correspondent_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Организация Корреспондентский счет')
    organization_current_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Организация Текущий счет')

    #Сведения о покупателе
    customer_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Покупатель Наименование')
    customer_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='Покупатель ИНН')
    customer_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='Покупатель КПП')
    customer_is_IP = models.BooleanField(default=False, verbose_name='Покупатель является ИП')
    customer_main_state_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Покупатель Основной государственный регистрационный номер')
    customer_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Покупатель Адрес')
    customer_telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Покупатель Телефон')
    customer_conventional_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Покупатель условное наименование')

    #Банковские реквизиты покупателя
    customer_bik = models.CharField(max_length=9, blank=True, null=True, verbose_name='Покупатель БИК')
    customer_bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Покупатель Наименование банка')
    customer_place_of_registration = models.CharField(max_length=100, blank=True, null=True, verbose_name='Покупатель Место нахождения')
    customer_correspondent_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Покупатель Корреспондентский счет')
    customer_current_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Покупатель Текущий счет')

    #Сведения о грузополучателе
    consignee_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Грузополучатель Наименование')
    consignee_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='Грузополучатель ИНН')
    consignee_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='Грузополучатель КПП')
    consignee_is_IP = models.BooleanField(default=False, verbose_name='Грузополучатель является ИП')
    consignee_main_state_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Грузополучатель Основной государственный регистрационный номер')
    consignee_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Грузополучатель Адрес')
    consignee_telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Грузополучатель Телефон')

    #Дополнительная информация
    purpose_of_payment = models.CharField(max_length=100, blank=True, null=True, verbose_name='Цель платежа')
    payment_for = models.CharField(max_length=100, blank=True, null=True, verbose_name='Платеж за')
    agreement = models.CharField(max_length=100, blank=True, null=True, verbose_name='Договор')
    vat_rate = models.ForeignKey(VatRate, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ставка НДС')
    printed_form = models.CharField(max_length=100, blank=True, null=True, verbose_name='Печатная форма')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Валюта')
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Скидка')

    class Meta:
        verbose_name = 'Счет на оплату'
        verbose_name_plural = 'Счет на оплату'
    
    
    
    
    
