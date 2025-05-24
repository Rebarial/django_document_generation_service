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
        "organization.accountant_name": ("AI", 22),
        "purpose_of_payment":("A",15),
    },
    "Concatenation": {
        "organization.address": ("A", 8),
        "organization.inn": ("A", 8),
        "organization.ogrn": ("A", 8),
        "organization_bank.name": ("A", 8),
        "organization_bank.address": ("A", 8),
        "organization_bank.correspondent_account": ("A", 8),
        "organization_bank.bic": ("A", 8),

        "buyer.address": ("AY", 8),
        "buyer.inn": ("AY", 8),
        "buyer.ogrn": ("AY", 8),
        "buyer_bank.name": ("AY", 8),
        "buyer_bank.address": ("AY", 8),
        "buyer_bank.correspondent_account": ("AY", 8),
        "buyer_bank.bic": ("AY", 8),
    },
    "Images":[
        {
            "type": "stamp",
            "cell": ("CM", 19),
            "width": 110,
            "height": 110
        },
        {
            "type": "signature",
            "cell": ("BQ", 18),
            "width": 110,
            "height": 70
        },
    ],
    "Defoult_items": #Кортеж словарей, содержащих информацию для вставки строк в документ
    (
        {
            "items_model_name": "items_docs", #Название таблицы из которой будут браться строки
            "cell_itmes_number": 13, #Номер строки, с которой начинается вставка
            "sum_cell": ("CN", 14),
            "sum_str": ("A", 14),
            "row_number": "A",
            "items_content": #Содержание вставки ключ – название поля модели, значение – буква ячейки            
            {
                "name": "E",
                "price": "BB",
                "quantity": "BP",
                "unit": "BY",
                "sum": "CN"
            },
            "static_content":
            {
                "vat_rate.name": "CG",
            },
        },
    ),
    "Custom_data" :
    {
        "vat_rate_sum": ("A", 14),
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