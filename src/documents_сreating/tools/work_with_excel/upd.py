from .base import BaseExcelDocumentCreate
from documents_сreating.models.base import BaseModel
from openpyxl import load_workbook
from openpyxl.worksheet.pagebreak import Break
from openpyxl.worksheet.worksheet import Worksheet
from ..layout_parameters_dictionary.upd import upd_dict
from io import BytesIO
from documents_сreating.models.organization import Organization
import locale
from typing import Callable

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

class UPDExcelDocumentCreate(BaseExcelDocumentCreate):

    def __init__(self, document_dict: dict, template_path: str):
        super().__init__(document_dict, template_path)

    def get_cell_ref(self, key: tuple[str, int], cell_itmes_number: int, offset: int) -> str:
        """
        Возвращает строковое представление ссылки excel на основе кортежа, учитывая смещение при добавлении items
        """
        num = key[1]
        if cell_itmes_number and num > cell_itmes_number: 
            num += offset
        return f"{key[0]}{num}"

    def find_nearest_lesser_or_equal(self, numbers: tuple, target: int) -> int:

        lesser_numbers = [num for num in numbers if num <= target]
        
        if not lesser_numbers:
            return None
        
        return max(lesser_numbers)

    def add_rows_break(self, sheet: Worksheet, break_points: list, offset: int, items_row: int) -> None:

        break_points = [point if point <= items_row else point + offset for point in break_points]

        last_row = sheet.max_row + 3
        i = 1
        start_items_row = items_row - 2 # -2: Добавил шапку и 0 строку
        end_items_row = items_row + offset + 1 # + 1: Добавил колонку итогов
        row_height_sum = 0
        start_id = 0
        max_height_on_list = 530 #530 - размер листа

        while i <= last_row:
            
            if not row_height_sum: #Для отладки
                start_id = i

            #Если превышаем максимальный размер, то разрываем на ближайшем break_point < i
            if sheet.row_dimensions[i].height:
                row_height_sum += sheet.row_dimensions[i].height
            else:
                row_height_sum += 11.25
            
            if row_height_sum < max_height_on_list:
                i += 1
            else:
                if start_items_row <= i <= end_items_row:
                    i += 1
                    row_height_sum = 0
                else:
                    break_point = self.find_nearest_lesser_or_equal(break_points, i)
                    if not break_point:
                        row_height_sum = 0
                        i += 1
                    else:
                        i = break_point
                        sheet.row_breaks.append(Break(id=i))

                        '''
                        #Отладочная код, возможно надо будет вернутся к функции
                        test_sum = 0
                        for j in range(start_id, i):
                            if sheet.row_dimensions[j].height:
                                test_sum += sheet.row_dimensions[j].height
                            else:
                                test_sum += 11.25
                        print(f'test sum = {test_sum}')
                        '''
                        i += 1
                        row_height_sum = 0
        #print(f'{start_id} : {i} : {row_height_sum}: {self.find_nearest_lesser_or_equal(break_points, i)}')

    def create_excel_document(self, document: BaseModel, converter: Callable) -> BytesIO:

        if not converter:
            converter = self.toPDF_libre

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
