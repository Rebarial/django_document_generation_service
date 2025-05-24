from .invoice_for_payment import invoice_for_payment_excel_document_create
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment


models_dict = {
    'invoice' : {
        'engine': invoice_for_payment_excel_document_create,
        'model' : DocumentInvoiceForPayment,
    }
}

__all__ = [
    'invoice_for_payment_excel_document_create',
]
