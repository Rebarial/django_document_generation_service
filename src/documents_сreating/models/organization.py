from django.db import models
from .base import BaseModel
from django.conf import settings

class Organization(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', 
                             help_text='Выбор пользователя')

    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    full_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Полное наименование')
    conventional_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Условное наименование')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП')
    is_ip = models.BooleanField(default=False, verbose_name='организация является ИП')
    ogrn = models.CharField(max_length=15, blank=True, null=True, verbose_name='ОГРН/ОГРНИП')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Телефон')
    fax = models.CharField(max_length=11, blank=True, null=True, verbose_name='Организация Факс')
    director_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность руководителя')
    director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО руководителя')
    accountant_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО бухгалтера')
    stamp = models.ImageField(upload_to='organization_stamps/', blank=True, null=True, verbose_name='Печать')
    signature = models.ImageField(upload_to='organization_signatures/', blank=True, null=True, verbose_name='Подпись')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

class Status(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    
    class Meta:
        verbose_name = 'Статусы'
        verbose_name_plural = 'Статусы'
        ordering = ['id']

class StatusOrganization(BaseModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='status_org', verbose_name='Организация')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='org_status', verbose_name='Статус')

    class Meta:
        verbose_name = 'Статусы организаций'
        verbose_name_plural = 'Статусы организаций'
        ordering = ['organization']

class BankDetails(BaseModel):
    
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='bank_details', verbose_name='Реквизиты банка')
    bik = models.CharField(max_length=9, blank=True, null=True, verbose_name='БИК')
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name='Наименование')
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Место нахождения банка')
    correspondent_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Корреспондентский счет')
    current_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Текущий счет')

    class Meta:
        verbose_name = 'Банк организации'
        verbose_name_plural = 'Банк организации'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.current_account}"

"""
class Seller(Organization):
    
    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавец'
        ordering = ['name']

class Buyer(Organization):
    
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатель'
        ordering = ['name']

class Consignee(Organization):

    class Meta:
        verbose_name = 'Грузополучатель'
        verbose_name_plural = 'Грузополучатель'
        ordering = ['name']

class Consignor(Organization):

    class Meta:
        verbose_name = 'Грузоотправитель'
        verbose_name_plural = 'Грузоотправитель'
        ordering = ['name']
"""