utd_dict = {
    "Break_points": [
        24, 29, 32, 
    ],
    "Raw_data": {
        "number": ("AP", 2),
        "corr_number": ("AP", 4),
        "seller.address": ("AP", 7),
        "seller.inn": ("AP", 8),
        "seller.director_name": ("BS",25),
        "payment_document": ("AT", 11),
        "shipping_document": ("AX", 12),
        "buyer.name": ("DL", 6),
        "buyer.address": ("DL", 7),
        "buyer.inn": ("DL", 8),
        "currency": ("DP", 9),
        "transfer_basis": ("AW", 31),
        "transport_info": ("AJ", 33),
        "transfer_position": ("A", 36),
        "transfer_name": ("AZ", 36),
        "transfer_additional_info": ("A", 40),
        "transfer_responsible_position": ("A", 43),
        "transfer_responsible_name": ("AZ", 43),
        "receiver_position": ("CF", 36),
        "receiver_name": ("EE", 36),
        "receipt_additional_info": ("CF", 40),
        "receipt_responsible_position": ("CF", 43),
        "receipt_responsible_name": ("EE", 43),
    },
    "Concatenation": 
    {
        #"seller.status": ("AP", 6),
        "seller.name": ("AP", 6),
        "consignee.name": ("AP", 10),
        "consignee.address": ("AP", 10),
        "document_seller.name": ("A", 46),
        "document_seller.inn": ("A", 46),
        "document_seller.kpp": ("A", 46),
        "document_buyer.name": ("CF", 46),
        "document_buyer.inn": ("CF", 46),
        "document_buyer.kpp": ("CF", 46),
    },
    "Images":(
            {
                "type": "stamp",
                "cell": ("C", 43),
                "width": 110,
                "height": 110
            },
            {
                "type": "signature",
                "cell": ("AZ", 24),
                "width": 110,
                "height": 70
            },
            {
                "type": "signature",
                "cell": ("AD", 33),
                "width": 110,
                "height": 70},
            {
                "type": "signature",
                "cell": ("AD", 40),
                "width": 110,
                "height": 70
            },
    ),
    "Defoult_items": #Кортеж словарей, содержащих информацию для вставки строк в документ
    (
        {
            "items_model_name": "items_docs", #Название таблицы из которой будут браться строки
            "cell_itmes_number": 22, #Номер строки, с которой начинается вставка
            "sum_cell": ("DQ", 23),
            "items_content": #Содержание вставки ключ – название поля модели, значение – буква ячейки
            {
                "code": "A",
                "name": "R",
                "type_code": "AQ",
                "unit": "BA",
                "quantity": "BN",
                "price": "BU",
                "sum": "DQ",
                "country": "EJ",
                "gtd_number": "ET"
            },
        },
    ),
    "Date": 
    {
        "day":{
            "transfer_date": ("AL", 38),
            "receipt_date": ("DP", 38),
        },
        "month":{
            "transfer_date": ("AR", 38),
            "receipt_date": ("DV", 38),
        },
        "year":{
            "transfer_date": ("BP", 38),
            "receipt_date": ("ET", 38),
        },
        "fromat":{
            "date": ("BK", 2),
            "corr_date": ("BK", 4),
        }  
    },
    "Custom_data": #Представление данных, которые будут обрабатываться в конкретном документе.
    {
        "org_field": "seller.id",
        "separator": ", ",
    }
}