from django.db import models
from ..base import BaseModel
from ..reference import VatRate, Currency, DocumentType, SellerStatus
from .base import BaseDocument

class UTDItem(BaseModel):
    utd = models.ForeignKey('DocumentUTD', on_delete=models.CASCADE, related_name='items_docs', verbose_name='УПД')
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Код товара')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    type_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Код вида товара')
    unit = models.CharField(max_length=100, blank=True, null=True, verbose_name='Единица измерения')
    excise = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name='Акциз')
    quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Сумма')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна')
    gtd_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер ГТД')

    class Meta:
        verbose_name = 'Товар документа'
        verbose_name_plural = 'Товары документа'


class DocumentUTD(BaseDocument):
    #Счет-фактура
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер счет-фактуры')
    date = models.DateField(blank=True, null=True, verbose_name='Дата счет-фактуры')
    corr_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер исправления')
    corr_date = models.DateField(blank=True, null=True, verbose_name='Дата исправления')

    payment_document = models.CharField(max_length=500, blank=True, null=True, verbose_name='К платежно-расчетному документу')
    shipping_document = models.CharField(max_length=500, blank=True, null=True, verbose_name='Документ об отгрузке')
    
    # На авансовый платеж
    is_advance = models.BooleanField(default=False, verbose_name='Авансовый платеж')
    
    #Информация о продавце
    seller = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='seller_utd', verbose_name='Продавец')
    consignor = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='consignor_utd', verbose_name='Грузоотправитель')

    buyer = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='buyer_utd', verbose_name='Контрагент')
    consignee = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='consignee_utd', verbose_name='Грузополучатель')

    #Дополнительная информация
    contract_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Идентификатор гос. контракта')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Тип документа')
    vat_rate = models.ForeignKey(VatRate, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ставка НДС')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Валюта')
    print_form = models.CharField(max_length=255, blank=True, null=True, verbose_name='Печатная форма')

    #Основание передачи/получения и данные о транспортировке
    transfer_basis = models.CharField(max_length=100, blank=True, null=True, verbose_name='Основание передачи/получения')
    transport_info = models.CharField(max_length=100, blank=True, null=True, verbose_name='Данные о транспортировке и грузе')

    #Товар передал / услуги, результаты работ, права сдал
    transfer_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность передатчика')
    transfer_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО передатчика')
    transfer_date = models.DateField(blank=True, null=True, verbose_name='Дата отгрузки')
    transfer_additional_info = models.TextField(blank=True, null=True, verbose_name='Иные сведения об перемещении')

    #Ответственный
    transfer_responsible_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность ответственного за перемещение')
    transfer_responsible_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО ответственного за перемещение')

    #Товар (груз) получил / услуги, результаты работ, права принял
    receiver_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность получателя')
    receiver_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО получателя')
    receipt_date = models.DateField(blank=True, null=True, verbose_name='Дата получения (приемки)')
    receipt_additional_info = models.TextField(blank=True, null=True, verbose_name='Иные сведения о получении, приемке')

    #Ответственный
    receipt_responsible_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность ответственного за приемку')
    receipt_responsible_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО ответственного за приемку')

    #Продавец составитель документа
    document_seller = models.ForeignKey('Organization', on_delete=models.CASCADE, blank=True, null=True, related_name='document_seller_utd', verbose_name='Продавц-составитель')

    #Покупатель составитель документа
    document_buyer = models.ForeignKey('Organization', on_delete=models.CASCADE, blank=True, null=True, related_name='document_buyer_utd', verbose_name='Покупатель-составитель')

    is_stamp = models.BooleanField(default=False, verbose_name='Выводить печать')

    class Meta:
        verbose_name = 'УПД'
        verbose_name_plural = 'УПД'