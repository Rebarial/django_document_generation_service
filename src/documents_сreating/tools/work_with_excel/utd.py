from .base import BaseExcelDocumentCreate
from documents_сreating.models.base import BaseModel
from openpyxl import load_workbook
from ..layout_parameters_dictionary.utd import utd_dict
from io import BytesIO
from typing import Callable

class UTDExcelDocumentCreate(BaseExcelDocumentCreate):

    def __init__(self, document_dict: dict, template_path: str):
        super().__init__(document_dict, template_path)

    def create_pdf_document(self, document: BaseModel, converter: Callable) -> BytesIO:
        if not converter:
            converter = self.toPDF_libre

        return converter(self.create_excel_document(document))

    def create_excel_document(self, document: BaseModel, in_file = False) -> BytesIO:

        workbook = load_workbook(self.template_path)
        sheet = workbook.active
        offset = []

        self.fill_doc(document, sheet, offset, self.document_dict["Custom_data"]["org_field"])

        #!!Костыль для проверки на одинаковый ИНН продавца и грузоотправителя
        cell_consignor = "AP9"
        if self.get_nested_attribute(document, "seller.inn") == self.get_nested_attribute(document, "consignor.inn"):
            sheet[cell_consignor] = "он же"
        elif not self.get_nested_attribute(document, "consignor.inn"):
            sheet[cell_consignor] = "---"
        else:
            sheet[cell_consignor] = str(self.get_nested_attribute(document, "consignor.name")) + ", " + str(self.get_nested_attribute(document, "consignor.address"))
            value = sheet[cell_consignor].value
            self.calculate_row_height(value, sheet[cell_consignor].font, sheet.column_dimensions["AP"].width)
    
        #Добавляем разрывы в зависимости от занимаемого места
        if "Break_points" in self.document_dict:
            self.add_rows_break(sheet, self.document_dict["Break_points"], offset)

        #Для корректного отображения с toPDF_libre
        sheet.page_setup.scale = 99
   
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return output

utd_excel_document_create = UTDExcelDocumentCreate(
    document_dict=utd_dict,
    #template_path="documents_сreating\\templates\\excel_templates\\UPD\\UPD.xlsx"
    template_path="documents_сreating/templates/excel_templates/UPD/UPD.xlsx"
)
