from ..models import DocumentUPD
from rest_framework import viewsets
from rest_framework.decorators import action
from ..serializers import DocumentUPDSerializer
from ..tools.work_with_excel.upd import upd_excel_document_create
from django.http import HttpResponse
from typing import Callable

class DocumentUPDViewSet(viewsets.ModelViewSet):
    queryset = DocumentUPD.objects.all()
    serializer_class = DocumentUPDSerializer
    
    def create_doc(self, pk: int, func: Callable):
        document = DocumentUPD.objects.get(id=pk)

        excel_document = upd_excel_document_create.create_excel_document(document, func)

        doc_date = str(document.invoice_date) if document.invoice_date else ""
        doc_number = str(document.invoice_number) if document.invoice_number else ""

        response = HttpResponse(excel_document.read(), content_type='application/pdf')
        #response = HttpResponse(excel_document.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={doc_date} {doc_number} UPD.pdf'
        return response
    
    """
    @action(detail=True, methods=['get'], url_path='win32', url_name='win32')
    def create_document_win32(self, request, pk=None):
        return self.create_doc(pk, upd_excel_document_create.toPDF_win32)

    @action(detail=True, methods=['get'], url_path='spire', url_name='spire')
    def create_document_spire(self, request, pk=None):
        return self.create_doc(pk, upd_excel_document_create.toPDF_spire)
    """

    @action(detail=True, methods=['get'], url_path='libre', url_name='libre')
    def create_document_libre(self, request, pk=None):
        return self.create_doc(pk, upd_excel_document_create.toPDF_libre)
