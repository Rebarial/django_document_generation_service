from django.db import models
from .base import BaseModel

class Organization(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    full_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Полное наименование')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП')
    ogrn = models.CharField(max_length=15, blank=True, null=True, verbose_name='ОГРН')
    okpo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Код ОКПО')
    okved = models.CharField(max_length=20, blank=True, null=True, verbose_name='Код ОКВЭД')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    director_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность руководителя')
    director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО руководителя')
    accountant_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО бухгалтера')
    stamp = models.ImageField(upload_to='organization_stamps/', blank=True, null=True, verbose_name='Печать')
    signature = models.ImageField(upload_to='organization_signatures/', blank=True, null=True, verbose_name='Подпись')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']
