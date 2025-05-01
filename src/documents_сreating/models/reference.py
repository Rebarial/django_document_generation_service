from django.db import models
from .base import BaseModel

class VatRate(BaseModel):
    code = models.CharField(max_length=10, verbose_name='Код')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Ставка')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Ставка НДС'
        verbose_name_plural = 'Ставки НДС'
        ordering = ['code']

class Currency(BaseModel):
    code = models.CharField(max_length=3, verbose_name='Код')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    short_name = models.CharField(max_length=10, verbose_name='Сокращенное наименование')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['code']

class DocumentType(BaseModel):
    code = models.CharField(max_length=10, verbose_name='Код')
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'
        ordering = ['code']

class SellerStatus(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Статус продавца'
        verbose_name_plural = 'Статусы продавцов'
