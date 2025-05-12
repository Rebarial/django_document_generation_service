from .base import BaseExcelDocumentCreate
from documents_сreating.models.base import BaseModel
from openpyxl import load_workbook
from ..layout_parameters_dictionary.upd import upd_dict
from io import BytesIO
import locale
from typing import Callable

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

class UPDExcelDocumentCreate(BaseExcelDocumentCreate):

    def __init__(self, document_dict: dict, template_path: str):
        super().__init__(document_dict, template_path)

    def create_excel_document(self, document: BaseModel, converter: Callable) -> BytesIO:

        if not converter:
            converter = self.toPDF_libre

        workbook = load_workbook(self.template_path)
        sheet = workbook.active
        offset = 0
        cell_itmes_number = None

        fill_dict = self.fill_doc(document, sheet, offset, cell_itmes_number)
        cell_itmes_number = fill_dict["cell_itmes_number"]
        offset = fill_dict["offset"]

        #!!Костыль для проверки на одинаковый ИНН продавца и грузоотправителя
        cell_consignor = "AP9"
        if getattr(document, "seller_inn") == getattr(document, "consignor_inn"):
            sheet[cell_consignor] = "он же"
        elif not getattr(document, "consignor_inn"):
            sheet[cell_consignor] = "---"
        else:
            sheet[cell_consignor] = str(getattr(document, "consignor_name")) + ", " + str(getattr(document, "consignor_address"))
            value = sheet[cell_consignor].value
            #self.calculate_row_height(value, sheet[cell_consignor].font, sheet.column_dimensions["AP"].width)
    
        #Добавляем разрывы в зависимости от занимаемого места
        if "break_points" in self.document_dict:
            self.add_rows_break(sheet, self.document_dict["break_points"], offset, cell_itmes_number)

        #Для корректного отображения с toPDF_libre
        sheet.page_setup.scale = 99

        temp_file_name = 'temp.xlsx'
        
        
        workbook.save(temp_file_name)

        #Если нужен будет xlsx
        #buffer = BytesIO() 
        #workbook.save(buffer)
        #buffer.seek(0)

        return converter(temp_file_name)

upd_excel_document_create = UPDExcelDocumentCreate(
    document_dict=upd_dict,
    #template_path="documents_сreating\\templates\\excel_templates\\UPD\\UPD.xlsx"
    template_path="documents_сreating/templates/excel_templates/UPD/UPD.xlsx"
)
