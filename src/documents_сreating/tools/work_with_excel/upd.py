from .base import BaseExcelDocumentCreate
from openpyxl import load_workbook
from ..layout_parameters_dictionary.upd import upd_dict
from io import BytesIO
from documents_сreating.models.organization import Organization
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

class UPDExcelDocumentCreate(BaseExcelDocumentCreate):

    def __init__(self, document_dict, template_path):
        super().__init__(document_dict, template_path)
        self.cell_number_of_items = 0

    def get_cell_ref(self, key: tuple[str, int], cell_itmes_number: int, offset: int) -> str:
        num = key[1]
        if cell_itmes_number and num > cell_itmes_number: 
            num += offset
        return f"{key[0]}{num}"

    def create_excel_document(self, document):
        workbook = load_workbook(self.template_path)
        sheet = workbook.active
        offset = 0
        cell_itmes_number = None

        #!!Нужно добавить все колонки и подсчет сумм
        if "cell_itmes_number" in self.document_dict:
            cell_itmes_number = self.document_dict["cell_itmes_number"]
            offset = self.add_document_itmes(sheet, document.items_docs, cell_itmes_number)

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
                    sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key))

        #!!Необходимо добавить заполнение КПП если ИНН отсутствует
        if "concatenation" in self.document_dict:
            for key, cell_ref in self.document_dict["concatenation"].items():
                if hasattr(document, key) and getattr(document, key):
                    if sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)].value != None:
                        sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)].value += f", {getattr(document, key)}"
                    else:
                        sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key))

        #!!Изменить склонения месяцов дат
        if "date" in self.document_dict:
            for key, cell_ref in self.document_dict["date"]["day"].items():
                if hasattr(document, key) and getattr(document, key):
                    sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key).day)

            for key, cell_ref in self.document_dict["date"]["month"].items():
                if hasattr(document, key) and getattr(document, key):
                    sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key).strftime('%B'))

            for key, cell_ref in self.document_dict["date"]["year"].items():
                if hasattr(document, key) and getattr(document, key):
                    sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = str(getattr(document, key).year)

            for key, cell_ref in self.document_dict["date"]["fromat"].items():
                if hasattr(document, key) and getattr(document, key):
                    sheet[self.get_cell_ref(cell_ref, cell_itmes_number, offset)] = f'"{getattr(document, key).day}" {getattr(document, key).strftime("%B %Y г.")}'

        #!!Костыль для проверки на одинаковый ИНН продавца и грузоотправителя
        if getattr(document, "seller_inn") == getattr(document, "consignor_inn"):
            sheet["AP9"] = "он же"
        elif not getattr(document, "consignor_inn"):
            sheet["AP9"] = "---"
        else:
            sheet["AP9"] = str(getattr(document, "consignor_name")) + ", " + str(getattr(document, "consignor_address"))

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        return buffer

upd_excel_document_create = UPDExcelDocumentCreate(
    document_dict=upd_dict,
    template_path="documents_сreating\\templates\\excel_templates\\UPD\\UPD.xlsx"
)
