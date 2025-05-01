from django.db import models
from .base import BaseModel
from .organization import Organization
from .reference import VatRate, Currency, DocumentType, SellerStatus

class BaseDocument(BaseModel):
    pass

class PaymentDocument(BaseModel):
    upd = models.ForeignKey('DocumentUPD', on_delete=models.CASCADE, related_name='payment_docs', verbose_name='УПД')
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер документа')
    date = models.DateField(blank=True, null=True, verbose_name='Дата документа')

    class Meta:
        verbose_name = 'Платежно-расчетный документ'
        verbose_name_plural = 'Платежно-расчетные документы'

class ShipmentDocument(BaseModel):
    upd = models.ForeignKey('DocumentUPD', on_delete=models.CASCADE, related_name='shipment_docs', verbose_name='УПД')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование документа')
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер документа')
    date = models.DateField(blank=True, null=True, verbose_name='Дата документа')

    class Meta:
        verbose_name = 'Документ об отгрузке'
        verbose_name_plural = 'Документы об отгрузке'

class DocumentItem(BaseModel):
    upd = models.ForeignKey('DocumentUPD', on_delete=models.CASCADE, related_name='items_docs', verbose_name='УПД')
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Код товара')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    type_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Код вида товара')
    unit_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Код единицы измерения')
    excise = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name='Акциз')
    quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Сумма')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна')
    gtd_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер ГТД')

    class Meta:
        verbose_name = 'Товар документа'
        verbose_name_plural = 'Товары документа'

class DocumentUPD(BaseDocument):
    #Счет-фактура
    invoice_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер счет-фактуры')
    invoice_date = models.DateField(blank=True, null=True, verbose_name='Дата счет-фактуры')
    correction_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер исправления')
    correction_date = models.DateField(blank=True, null=True, verbose_name='Дата исправления')
    
    # На авансовый платеж
    is_advance = models.BooleanField(default=False, verbose_name='Авансовый платеж')
    
    #Информация о продавце
    seller_status = models.ForeignKey(SellerStatus, on_delete=models.CASCADE, related_name='seller_status', blank=True, null=True, verbose_name='Статус продавца')
    seller_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование продавца')
    seller_full_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Полное наименование продавца')
    seller_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИНН продавца')
    seller_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП продавца')
    seller_address = models.TextField(blank=True, null=True, verbose_name='Адрес продавца')
    seller_director_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность руководителя')
    seller_director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО руководителя')
    seller_accountant_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО бухгалтера')

    #Информация о грузоотправителе
    consignor_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование грузоотправителя')
    consignor_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИНН грузоотправителя')
    consignor_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП грузоотправителя')
    consignor_address = models.TextField(blank=True, null=True, verbose_name='Адрес грузоотправителя')
    consignor_director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО руководителя')

    #Информация о клиенте
    customer_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование клиента')
    customer_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИНН клиента')
    customer_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП клиента')
    customer_address = models.TextField(blank=True, null=True, verbose_name='Адрес клиента')
    customer_director_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Должность руководителя')
    customer_director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО руководителя')

    #Информация о грузополучателе
    consignee_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование грузополучателя')
    consignee_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИНН грузополучателя')
    consignee_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП грузополучателя')
    consignee_address = models.TextField(blank=True, null=True, verbose_name='Адрес грузополучателя')
    consignee_director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО руководителя')

    #Дополнительная информация
    contract_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Идентификатор гос. контракта')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Тип документа')
    vat_rate = models.ForeignKey(VatRate, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ставка НДС')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Валюта')
    print_form = models.CharField(max_length=255, blank=True, null=True, verbose_name='Печатная форма')

    #Основание передачи/получения и данные о транспортировке
    transfer_basis = models.TextField(blank=True, null=True, verbose_name='Основание передачи/получения')
    transport_info = models.TextField(blank=True, null=True, verbose_name='Данные о транспортировке и грузе')

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
    document_seller_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование продавца-составителя')
    document_seller_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИНН продавца-составителя')
    document_seller_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП продавца-составителя')

    #Покупатель составитель документа
    document_customer_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование покупателя-составителя')
    document_customer_inn = models.CharField(max_length=12, blank=True, null=True, verbose_name='ИНН покупателя-составителя')
    document_customer_kpp = models.CharField(max_length=9, blank=True, null=True, verbose_name='КПП покупателя-составителя')

    class Meta:
        verbose_name = 'УПД'
        verbose_name_plural = 'УПД'

