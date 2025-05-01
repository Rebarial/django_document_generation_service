from ..models import DocumentUPD
from rest_framework import viewsets
from rest_framework.decorators import action
from ..serializers import DocumentUPDSerializer
from ..tools.work_with_excel.upd import upd_excel_document_create
from django.http import HttpResponse

class DocumentUPDViewSet(viewsets.ModelViewSet):
    queryset = DocumentUPD.objects.all()
    serializer_class = DocumentUPDSerializer
    
    @action(detail=True, methods=['get'], url_path='download', url_name='download-document')
    def create_document(self, request, pk=None):
        
        document = DocumentUPD.objects.get(id=pk)

        excel_document = upd_excel_document_create.create_excel_document(document)

        doc_date = str(document.invoice_date) if document.invoice_date else ""
        doc_number = str(document.invoice_number) if document.invoice_number else ""

        response = HttpResponse(excel_document.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={doc_date} {doc_number} UPD.xlsx'
        return response
