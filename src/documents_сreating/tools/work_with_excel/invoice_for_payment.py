from .base import BaseExcelDocumentCreate
from documents_сreating.models.base import BaseModel
from openpyxl import load_workbook
from ..layout_parameters_dictionary.invoice_for_payment import invoice_for_payment_dict
from io import BytesIO
from documents_сreating.models.organization import Organization
import locale
from typing import Callable

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

class InvoiceForPaymentExcelDocumentCreate(BaseExcelDocumentCreate):

    def __init__(self, document_dict: dict, template_path: str):
        super().__init__(document_dict, template_path)

    def create_excel_document(self, document: BaseModel, converter: Callable) -> BytesIO:

        if not converter:
            converter = self.toPDF_libre

        workbook = load_workbook(self.template_path)
        sheet = workbook.active
        offset = 0
        cell_itmes_number = None

        #!!Нужно добавить все колонки и подсчет сумм
        if "cell_itmes_number" in self.document_dict:
            cell_itmes_number = self.document_dict["cell_itmes_number"] #Номер строки с которой начинаются строки товаров
            offset = self.add_document_itmes(sheet, document.items_docs, cell_itmes_number) #Количество строк товаров

        if "Images" in self.document_dict:

            organization = Organization.objects.filter(inn=document.seller_inn).first()

            #Добавление печати и подписи
            if organization:
                for image in self.document_dict["Images"]:
                    if hasattr(organization, image["type"]) and getattr(organization, image["type"]):
                        self.add_image(sheet, getattr(organization, image["type"]).name, image["width"], image["height"], self.get_cell_ref(image["cell"], cell_itmes_number, offset))

        #!!Необходимо добавить заполнение КПП если ИНН отсутствует
        if "raw_data" in self.document_dict:
            for key, cell_ref in self.document_dict["raw_data"].items():
                if hasattr(document, key) and getattr(document, key):
                    value = str(getattr(document, key))
                    cell = self.get_cell_ref(cell_ref, cell_itmes_number, offset)
                    sheet[cell] = value
                    self.row_height_from_content(sheet, value, cell)

        #!!Необходимо добавить заполнение КПП если ИНН отсутствует
        if "concatenation" in self.document_dict:
            for key, cell_ref in self.document_dict["concatenation"].items():
                if hasattr(document, key) and getattr(document, key):
                    cell = self.get_cell_ref(cell_ref, cell_itmes_number, offset)
                    if sheet[cell].value != None:
                        sheet[cell].value += f", {getattr(document, key)}"
                        value = sheet[cell].value
                        self.row_height_from_content(sheet, value, cell)
                    else:
                        sheet[cell] = str(getattr(document, key))
                        value = sheet[cell].value
                        self.row_height_from_content(sheet, value, cell)

        #!!Изменить склонения месяцов дат
        if "date" in self.document_dict:
            if "day" in self.document_dict["date"]:
                for key, cell_ref in self.document_dict["date"]["day"].items():
                    if hasattr(document, key) and getattr(document, key):
                        sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key).day)
            if "month" in self.document_dict["date"]:
                for key, cell_ref in self.document_dict["date"]["month"].items():
                    if hasattr(document, key) and getattr(document, key):
                        sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key).strftime('%B'))

            if "year" in self.document_dict["date"]:
                for key, cell_ref in self.document_dict["date"]["year"].items():
                    if hasattr(document, key) and getattr(document, key):
                        sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key).year)

            if "fromat" in self.document_dict["date"]:
                for key, cell_ref in self.document_dict["date"]["fromat"].items():
                    if hasattr(document, key) and getattr(document, key):
                        sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = f'"{getattr(document, key).day}" {getattr(document, key).strftime("%B %Y г.")}'

        #!!Костыль для проверки на одинаковый ИНН продавца и грузоотправителя
        #cell_consignor = "AP9"
        #if getattr(document, "seller_inn") == getattr(document, "consignor_inn"):
        #    sheet[cell_consignor] = "он же"
        #elif not getattr(document, "consignor_inn"):
        #    sheet[cell_consignor] = "---"
       # else:
        #    sheet[cell_consignor] = str(getattr(document, "consignor_name")) + ", " + str(getattr(document, "consignor_address"))
        #    value = sheet[cell_consignor].value
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

invoice_for_payment_excel_document_create = InvoiceForPaymentExcelDocumentCreate(
    document_dict=invoice_for_payment_dict,
    #template_path="documents_сreating\\templates\\excel_templates\\UPD\\UPD.xlsx"
    template_path="documents_сreating/templates/excel_templates/UPD/invoice_for_payment.xlsx"
)
