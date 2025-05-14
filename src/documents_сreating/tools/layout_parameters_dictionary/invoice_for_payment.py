invoice_for_payment_dict = {
    "Break_points": [
        19
    ],
    "Raw_data": {
        "organization_name" : [("A", 5), ("A", 7)],
        "customer_name" : ("AY", 7),
        "purpose_of_payment" : ("A", 15),
        "organization_director_name" : ("AI", 20),
        "organization_director_position": ("A", 20),
        "organization_accountant_name": ("AI", 22)
    },
    "Concatenation": {
        "organization_address": ("A", 8),
        "organization_inn": ("A", 8),
        "organization_main_state_number": ("A", 8),
        "organization_bank_name": ("A", 8),
        "organization_bank_place_of_registration": ("A", 8),
        "organization_correspondent_account": ("A", 8),
        "organization_bik": ("A", 8),

        "customer_address": ("AY", 8),
        "customer_inn": ("AY", 8),
        "customer_main_state_number": ("AY", 8),
        "customer_bank_name": ("AY", 8),
        "customer_place_of_registration": ("AY", 8),
        "customer_correspondent_account": ("AY", 8),
        "customer_bik": ("A", 8),
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
        "inn_field": "organization_inn",
        "invoice_organization_info_cell_number": 1,
        "invoice_organization_info_items":{
            "info": "A",
        },
        "invoice_organization_info_value":(
            "organization_name", 
            "organization_address",
            "organization_inn",
            "organization_main_state_number",
        ),
        "document_name": {
            "cell": ("A", 10),
            "number": "invoice_for_payment_number",
            "date": "invoice_for_payment_data"
        }
    }
}