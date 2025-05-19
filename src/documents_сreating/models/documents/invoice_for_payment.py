from django.db import models
from ..base import BaseModel
from ..reference import VatRate, Currency, DocumentType, SellerStatus
from .base import BaseDocument
from django.conf import settings


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', 
                             help_text='Выбор пользователя')

    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер')
    date = models.DateField(blank=True, null=True, verbose_name='Дата')

    #Информация об организациях
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='organization', verbose_name='Организация')
    organization_bank = models.ForeignKey('BankDetails', on_delete=models.CASCADE, related_name='organization_bank_details', verbose_name='Реквизиты банка организации')

    buyer = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='buyer', verbose_name='Организация')
    buyer_bank = models.ForeignKey('BankDetails', on_delete=models.CASCADE, related_name='buyer_bank_details', verbose_name='Реквизиты банка покупателя')

    consignee = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='consignee', verbose_name='Грузополучатель')

    #Дополнительная информация
    purpose_of_payment = models.CharField(max_length=250, blank=True, null=True, verbose_name='Цель платежа')
    payment_for = models.CharField(max_length=250, blank=True, null=True, verbose_name='Платеж за')
    agreement = models.CharField(max_length=250, blank=True, null=True, verbose_name='Договор')
    vat_rate = models.ForeignKey(VatRate, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ставка НДС')
    printed_form = models.CharField(max_length=100, blank=True, null=True, verbose_name='Печатная форма')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Валюта')
    discount = models.CharField(max_length=6, blank=True, null=True, verbose_name='Скидка')
    additional_info = models.TextField(blank=True, null=True, verbose_name='Иные сведения')
    is_stamp = models.BooleanField(default=False, verbose_name='Выводить печать')

    class Meta:
        verbose_name = 'Счет на оплату'
        verbose_name_plural = 'Счет на оплату'