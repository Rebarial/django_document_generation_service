invoice_for_payment_dict = {
    "break_points": [
        19
    ],
    "cells_settings": {
        "column_size": 0.55,
        "first_column": "A",
        "last_column": "FI",
        },
    "raw_data": {
        "organization_name" : [("A", 5), ("A", 7)],
        "customer_name" : ("AY", 7),
        "purpose_of_payment" : ("A", 15),
        "organization_director_name" : ("AI", 20),
        "organization_director_position": ("A", 20),
        "organization_accountant_name": ("AI", 22)
    },
    #"Images":(
    #),
    "cell_itmes_number": 13,
    "items":{
        "name": "E",
        "price": "BB",
        "quantity": "BP",
        "unit": "BY",
        "sum": "CN"
    },
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
    "concatenation": {
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
    "document_name": {
        "cell": ("A", 10),
        "number": "invoice_for_payment_number",
        "date": "invoice_for_payment_data"
    }

}