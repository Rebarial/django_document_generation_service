# Document generation service
Приложение для создания документов. Написано с использованием django.

## Реализовано
 - админка http://127.0.0.1:8000/admin/
 - прифиль пользователя
 - создание документов упд
 - создание документов счет на оплату
 - создание организаций
 - создание банков

## Сервер
 - админка http://147.45.110.79:8000/admin/ (данные от админа логин: admin; пароль: admin) 
 - главная страница: http://147.45.110.79:8000


## Установка
Необходим docker и docker-copose

``` bash
git clone https://github.com/Rebarial/django_document_generation_service

cd django_document_generation_service

docker-compose up --build --force-recreate -d
```
## Используемые библиотеки

 - Django, djangorestframework – основа приложения
 - dotenv – загрузка .env переменных
 - openpyxl – работа с excel файлами
 - subprocess – вызов libreoffice для конвертации в pdf

## Сущности
 - Валюты
 - Ставки НДС
 - Статусы продавцов
 - Типы документов
 - Организации
 - Документы УПД

## Структура и функции (лучше посмотреть в Руководство пользователя.docx)
 - Сервиc: src\documents_creating
   - Шаблоны эксель документов: templates\excel_templates
   - Словари для заполнения документа: tools\layout_parameters_dictionary
   - Инструменты создания эксель документов: tools\work_with_excel
      - base.py
        - class BaseExcelDocumentCreate(ABC): – Основной класс содержащий методы для создания документов
          - def __init__(self, document_dict: dict, template_path: str) – Инициализация класса, необходимо заполнить словарь для заполнения документа и путь к шаблону
          - @abstractmethod def create_excel_document(self, document: BaseModel) -> BinaryIO: – Абстрактный метод создания документов PS На данный момент в единственной реализации возвращается PDF
          - def get_cell_ref(self, key: tuple[str, int], cell_itmes_number: int, offset: int) -> str: – Возвращает строковое представление ссылки excel на основе кортежа, учитывая смещение при добавлении items
          - def find_nearest_lesser_or_equal(self, numbers: tuple, target: int) -> int: – Возвращает ближайшую точку разрыва из листа точек разрыва
          - def add_rows_break(self, sheet: Worksheet, break_points: list, offset: int, items_row: int) -> None: – Добавляет разрывы в лист excel, если не помещается на страницу
            - Использует: find_nearest_lesser_or_equal
          - def add_image(self, sheet: Worksheet, img_file_path: str, width: int, height: int, cell: str) -> None: – Добавляет картинку на лист excel
          - def add_document_itmes(self, sheet: Worksheet, items: BaseModel, cell_itmes_number: int) -> int: – Добавляет строки в таблицу на лист excel, возвращает количество добавленных строк
            - Использует: self.document_dict, self.calculate_row_height
          - def calculate_row_height(self, text: str, font: Font, column_width: float) -> float: – Возвращает высоту строки в зависимости от содержания
          - def row_height_from_content(self, sheet: Worksheet, value: str, cell_ref: str) -> None: – Изменяет высоту строки в зависимости от содержания
            - Использует: self.calculate_row_height, self.get_merged_column_count
          - def get_merged_column_count(self, sheet: Worksheet, cell_ref: str) -> int: – Возвращает количество столбцов в объединении по ссылки на ячейку
          - def read_and_return_file(self, file_path: str) -> BytesIO: – Считывает данные из файла и возвращает в виде BytesIO
          - def toPDF_libre(self, file_path: str) -> BytesIO: – Конвертирует xlsx в pdf, используя subprocess libreoffice
            - Использует: self.read_and_return_file
        - upd.py
          - class UPDExcelDocumentCreate(BaseExcelDocumentCreate): – Класс для создания UPD документов
            - def create_excel_document(self, document: BaseModel, converter: Callable) -> BytesIO:
              - Использует: self.add_document_itmes, self.add_image, self.get_cell_ref, self.row_height_from_content, self.add_rows_break, self.toPDF_libre
   - DRF viewsets: api\
     - class DocumentUPDViewSet(viewsets.ModelViewSet):
       - def create_doc(self, pk: int, func: Callable): – создает документ и возвращает пользователю файл
         - Использует: UPDExcelDocumentCreate.create_excel_document
       - @action(detail=True, methods=['get'], url_path='libre', url_name='libre') def create_document_libre(self, request, pk=None): – API действие создает документ и возвращает пользователю файл
         - Использует: BaseExcelDocumentCreate.toPDF_libre, self.create_doc
   - Django-models: models\
     - base.py
       - class BaseModel(models.Model)
     - documents.py
       - class BaseDocument(BaseModel):
       - class PaymentDocument(BaseModel):
       - class ShipmentDocument(BaseModel):
       - class DocumentItem(BaseModel):
       - class DocumentUPD(BaseDocument):
         - Использует: PaymentDocument, ShipmentDocument, DocumentItem
     - organization.py
       - class Organization(BaseModel):
     - reference.py
       - class VatRate(BaseModel):
       - class Currency(BaseModel):
       - class DocumentType(BaseModel):
       - class SellerStatus(BaseModel):
      
## Узкие места
 - tools\work_with_excel\base.py
   - get_merged_column_count(sheet, cell_ref) – Перебирает все объединенные колонки пока не найдет ту, которая содержит cell_ref. Используется везде при вставки текстовых данных в excel
   - toPDF_libre(file_path) – Возможны ошибки с доступом к файлу (например, если файл уже открыт другим процессом)
 - tools\work_with_excel\upd.py
   - create_excel_document(document, converter) – Считывает данные с шаблона xlsx возможны проблемы с доступом

