from ..models import DocumentUTD, DocumentInvoiceForPayment
from rest_framework import viewsets
from rest_framework.decorators import action
from ..serializers import DocumentUTDSerializer, DocumentInvoiceForPaymentSerializer
from ..tools.work_with_excel.utd import utd_excel_document_create
from ..tools.work_with_excel.invoice_for_payment import invoice_for_payment_excel_document_create
from django.http import HttpResponse
from typing import Callable

class DocumentViewSet(viewsets.ModelViewSet):
    model = None
    document_create = None

    def create_doc(self, pk: int, func: Callable):
        document = self.model.objects.get(id=pk)

        excel_document = self.document_create.create_excel_document(document, func)

    #    doc_date = str(document.invoice_date) if document.invoice_date else ""
    #    doc_number = str(document.invoice_number) if document.invoice_number else ""

        response = HttpResponse(excel_document.read(), content_type='application/pdf')
        #response = HttpResponse(excel_document.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        #response['Content-Disposition'] = f'attachment; filename={doc_date} {doc_number} UPD.pdf'
        response['Content-Disposition'] = f'attachment; filename=test UPD.pdf'
        return response

class DocumentUTDViewSet(DocumentViewSet):
    queryset = DocumentUTD.objects.all()
    serializer_class = DocumentUTDSerializer
    model = DocumentUTD
    document_create = utd_excel_document_create

    @action(detail=True, methods=['get'], url_path='libre', url_name='libre')
    def create_document_libre(self, request, pk=None):
        return self.create_doc(pk, utd_excel_document_create.toPDF_libre)

class DocumentInvoiceForPaymentViewSet(DocumentViewSet):
    queryset = DocumentInvoiceForPayment.objects.all()
    serializer_class = DocumentInvoiceForPaymentSerializer
    model = DocumentInvoiceForPayment
    document_create = invoice_for_payment_excel_document_create

    @action(detail=True, methods=['get'], url_path='libre', url_name='libre')
    def create_document_libre(self, request, pk=None):
        return self.create_doc(pk, utd_excel_document_create.toPDF_libre)
