# Document generation service
Приложение для создания документов. Написано с использованием django.

## Реализовано
 - админка http://127.0.0.1:8000/admin/
 - APIView для документов UPD http://127.0.0.1:8000/api/upd/
 - частично реализовано создание UPD документа в xlsx формате http://127.0.0.1:8000/api/upd/{id} (extra actions) или http://127.0.0.1:8000/api/upd/{id}/download
## Установка
Необходим docker и docker-copose

``` bash
git clone https://github.com/Rebarial/django_document_generation_service

cd django_document_generation_service

docker-compose up --build --force-recreate -d
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
