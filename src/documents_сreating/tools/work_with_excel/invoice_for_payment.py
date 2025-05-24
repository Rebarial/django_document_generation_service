from .base import BaseExcelDocumentCreate
from documents_сreating.models.base import BaseModel
from openpyxl import load_workbook
from ..layout_parameters_dictionary.invoice_for_payment import invoice_for_payment_dict
from io import BytesIO
from typing import Callable

class InvoiceForPaymentExcelDocumentCreate(BaseExcelDocumentCreate):

    def __init__(self, document_dict: dict, template_path: str):
        super().__init__(document_dict, template_path)

    def create_pdf_document(self, document: BaseModel, converter: Callable) -> BytesIO:
        if not converter:
            converter = self.toPDF_libre

        return converter(self.create_excel_document(document))


    def create_excel_document(self, document: BaseModel, in_file = False) -> BytesIO:

        workbook = load_workbook(self.template_path)
        sheet = workbook.active
        sheet.title = f'Счет на оплату №{document.number} от {document.date}'
        offset = []

        if "document_name" in self.document_dict["Custom_data"]:

            number = self.document_dict["Custom_data"]["document_name"]["number"]
            if hasattr(document, number) and self.get_nested_attribute(document, number):
                sheet[self.get_cell_ref(self.document_dict["Custom_data"]["document_name"]["cell"], offset)].value += self.get_nested_attribute(document, number)

            date = self.document_dict["Custom_data"]["document_name"]["date"]
            if hasattr(document, date) and self.get_nested_attribute(document, date):
                sheet[self.get_cell_ref(self.document_dict["Custom_data"]["document_name"]["cell"], offset)].value += f' от {self.get_nested_attribute(document, date).day}" {self.get_nested_attribute(document, date).strftime("%B %Y г.")}'
           

        invoice_organization_info_dict_value = []
        for item in self.document_dict["Custom_data"]["invoice_organization_info_value"]:
            val = self.get_nested_attribute(document, item)
            if val:
                #print(self.get_nested_attribute(document, 'organization'))
                invoice_organization_info_dict_value.append({"info": str(val)})

        offset.append({
                "cell_itmes_number": self.document_dict["Custom_data"]["invoice_organization_info_cell_number"],
                "offset": self.add_document_itmes(
                    sheet=sheet,
                    items=invoice_organization_info_dict_value,
                    offsets=offset, 
                    items_dict={
                        "items_content": self.document_dict["Custom_data"]["invoice_organization_info_items"],
                        "cell_itmes_number": self.document_dict["Custom_data"]["invoice_organization_info_cell_number"]
                        },
                    height_orientation_name = "info",
                    height_orientation_column = "A",
                )
        })

        cell = self.get_cell_ref(self.document_dict["Custom_data"]["vat_rate_sum"], offset)
        sheet[cell] = "Итого (" + document.vat_rate.name + "):\n"

        fill_dict = self.fill_doc(document, sheet, offset, self.document_dict["Custom_data"]["inn_field"])

        #Добавляем разрывы в зависимости от занимаемого места
        if "Break_points" in self.document_dict:
            self.add_rows_break(sheet, self.document_dict["Break_points"], offset)

        #Для корректного отображения с toPDF_libre
        sheet.page_setup.scale = 99
   
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return output


invoice_for_payment_excel_document_create = InvoiceForPaymentExcelDocumentCreate(
    document_dict=invoice_for_payment_dict,
    #template_path="documents_сreating\\templates\\excel_templates\\UPD\\UPD.xlsx"
    template_path="documents_сreating/templates/excel_templates/UPD/invoice_for_payment.xlsx"
)
