from .invoice_for_payment import invoice_for_payment_excel_document_create
from .utd import utd_excel_document_create
from documents_сreating.models import DocumentInvoiceForPayment, DocumentUTD


models_dict = {
    'invoice' : {
        'engine': invoice_for_payment_excel_document_create,
        'model' : DocumentInvoiceForPayment,
        'name': "Счет на оплату"
    },
    'utd' : {
        'engine': utd_excel_document_create,
        'model' : DocumentUTD,
        'name': "Универсальный передаточный документ"
    }
}

__all__ = [
    'invoice_for_payment_excel_document_create',
]
