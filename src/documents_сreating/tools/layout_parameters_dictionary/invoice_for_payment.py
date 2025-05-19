invoice_for_payment_dict = {
    "Break_points": [
        19
    ],
    "Raw_data": {
        "organization.name" : [("A", 5), ("A", 7)],
        "buyer.name" : ("AY", 7),
        "purpose_of_payment" : ("A", 15),
        "organization.director_name" : ("AI", 20),
        "organization.director_position": ("A", 20),
        "organization.accountant_name": ("AI", 22)
    },
    "Concatenation": {
        "organization.address": ("A", 8),
        "organization.inn": ("A", 8),
        "organization.ogrn": ("A", 8),
        "organization_bank.name": ("A", 8),
        "organization_bank.address": ("A", 8),
        "organization_bank.correspondent_account": ("A", 8),
        "organization_bank.bik": ("A", 8),

        "buyer.address": ("AY", 8),
        "buyer.inn": ("AY", 8),
        "buyer.ogrn": ("AY", 8),
        "buyer_bank.name": ("AY", 8),
        "buyer_bank.address": ("AY", 8),
        "buyer_bank.correspondent_account": ("AY", 8),
        "buyer_bank.bik": ("A", 8),
    },
    "Images":[
        {
            "type": "stamp",
            "cell": ("CU", 21),
            "width": 110,
            "height": 110
        },
        {
            "type": "signature",
            "cell": ("CB", 20),
            "width": 110,
            "height": 70
        },
    ],
    "Defoult_items": #Кортеж словарей, содержащих информацию для вставки строк в документ
    (
        {
            "items_model_name": "items_docs", #Название таблицы из которой будут браться строки
            "cell_itmes_number": 13, #Номер строки, с которой начинается вставка
            "items_content": #Содержание вставки ключ – название поля модели, значение – буква ячейки
            {
                "name": "E",
                "price": "BB",
                "quantity": "BP",
                "unit": "BY",
                "sum": "CN"
            },
        },
    ),
    "Custom_data" :
    {
        "inn_field": "organization.inn",
        "invoice_organization_info_cell_number": 1,
        "invoice_organization_info_items":{
            "info": "A",
        },
        "invoice_organization_info_value":(
            "organization.name", 
            "organization.address",
            "organization.inn",
            "organization.ogrn",
        ),
        "document_name": {
            "cell": ("A", 10),
            "number": "number",
            "date": "date"
        }
    }
}