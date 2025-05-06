# Document generation service
Приложение для создания документов. Написано с использованием django.

## Реализовано
 - админка http://127.0.0.1:8000/admin/
 - APIView для документов UPD http://127.0.0.1:8000/api/upd/
 - частично реализовано создание UPD документа в xlsx формате http://127.0.0.1:8000/api/upd/{id} (extra actions) или http://127.0.0.1:8000/api/upd/{id}/download
## Установка

``` bash
git clone https://github.com/Rebarial/django_document_generation_service

cd django_document_generation_service
```
По желанию создайте виртуальное окружение

Windows:
``` bash
python -m venv venv

venv\Scripts\activate
```
Linux/macOS:
``` bash
python3 -m venv venv

source venv/bin/activate
```

Измените SECRET_KEY в django_document_generation_service/.env

``` bash

python -m pip install -r requirements.txt

cd src

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

## Сущности
 - Валюты
 - Ставки НДС
 - Статусы продавцов
 - Типы документов
 - Организации
 - Документы УПД

## Структура
 - Сервиc: src\documents_creating
   - Шаблоны эксель документов: templates\excel_templates
   - Словари для заполнения документа: tools\layout_parameters_dictionary
   - Инструменты создания эксель документов: tools\work_with_excel
   - DRF viewsets: api\
   - Django-models: models\
