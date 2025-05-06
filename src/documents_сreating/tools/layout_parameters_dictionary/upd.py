upd_dict = {
    "break_points": [
        24, 29, 32, 
    ],
    #Не пригодилось, у всех столбцов константый размер, в python = 1
    "cells_settings": {
        "column_size": 0.55,
        "first_column": "A",
        "last_column": "FI",
        },
    "raw_data": {
        "invoice_number": ("AP", 2),#"AP2",
        "correction_number": ("AP", 4),#"AP4",
        "seller_address": ("AP", 7),#"AP7",
        "seller_inn": ("AP", 8),#"AP8",
        "DocumentUPD": ("AT", 11),#"AT11",
        "ShipmentDocument": ("AX", 12),#"AX12",
        "customer_name": ("DL", 6),#"DL6",
        "customer_address": ("DL", 7),#"DL7",
        "customer_inn": ("DL", 8),#"DL8",
        "currency": ("DP", 9),#"DP9",
        "transfer_basis": ("AW", 31),#"AW31",
        "transport_info": ("AJ", 33),#"AJ33",
        "transfer_position": ("A", 36),#"A36",
        "transfer_name": ("AZ", 36),#"AZ36",
        "transfer_additional_info": ("A", 40),#"A40",
        "transfer_responsible_position": ("A", 43),#"A43",
        "transfer_responsible_name": ("AZ", 43),#"AZ43",
        "receiver_position": ("CF", 36),#"CF36",
        "receiver_name": ("EE", 36),#"EE36",
        "receipt_additional_info": ("CF", 40),#"CF40",
        "receipt_responsible_position": ("CF", 43),#"CF43",
        "receipt_responsible_name": ("EE", 43),#"EE43",
    },
    "Images":(
            {
                "type": "stamp",
                "cell": ("C", 43),
                "width": 120,
                "height": 120
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
    "ShipmentDocument":{
        "ShipmentDocument": ("AX", 12),#"AX12",
        "ShipmentDocumentDate": ("AX", 12),#"AX12",
        "ShipmentDocumentNumber": ("AX", 12),#"AX12",
    },
    "cell_itmes_number": 22,
    "items":{
        "code": "A",
        "name": "R",
        "type_code": "AQ",
        "quantity": "BN",
        "price": "BU",
        "amount": "CE",
        "country": "ED", #counry id
        "ET": "gtd_number"
    },
    "concatenation": {
        "seller_status": ("AP", 6),#"AP6",
        "seller_name": ("AP", 6),#"AP6",
        #"consignor_name": ("AP", 9),#"AP9", Проверка на одинаковый ИНН
        #"consignor_address": ("AP", 9),#"AP9",
        "consignee_name": ("AP", 10),#"AP10",
        "consignee_address": ("AP", 10),#"AP10",
        "document_seller_name": ("A", 46),#"A46",
        "document_seller_inn": ("A", 46),#"A46",
        "document_seller_kpp": ("A", 46),#"A46",
        "document_customer_name": ("CF", 46),# "CF46",
        "document_customer_inn": ("CF", 46),#"CF46",
        "document_customer_kpp": ("CF", 46),#"CF46",
    },
    "date": {
        "day":{
            "transfer_date": ("AL", 38),#"AL38", #Day
            "receipt_date": ("DP", 38),#"DP38", #Day
        },
        "month":{
            "transfer_date": ("AR", 38),#"AR38", #Month
            "receipt_date": ("DV", 38),#"DV38", #Month
        },
        "year":{
            "transfer_date": ("BP", 38),#"BP38", #Year
            "receipt_date": ("ET", 38),#"ET38", #Year
        },
        "fromat":{
            "invoice_date": ("BK", 2),
            "correction_date": ("BK", 4),
        }
        
    }
}