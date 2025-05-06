from abc import ABC, abstractmethod
import os
from io import BytesIO
from documents_сreating.models.base import BaseModel
from openpyxl.utils import range_boundaries, get_column_letter
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font
from django.core.files.storage import default_storage
from typing import BinaryIO
import math
import subprocess

class BaseExcelDocumentCreate(ABC):
    """
    Базовый класс для создания excel документов
    """

    def __init__(self, document_dict: dict, template_path: str):
        self.document_dict: dict = document_dict
        self.template_path: str = template_path

    @abstractmethod
    def create_excel_document(self, document: BaseModel) -> BinaryIO:
        """
        Создает excel документ на основе шаблона и словаря заполнения
        PS сейчас возвращает pdf
        """
        pass

    def add_image(self, sheet: Worksheet, img_file_path: str, width: int, height: int, cell: str) -> None:
        """
        Вставляет картинку в таблицу excel
        """
        with default_storage.open(img_file_path, 'rb') as stamp_file:
                binary_image = BytesIO(stamp_file.read())
        img = XLImage(binary_image)
        img.width = width
        img.height = height
        sheet.add_image(img, cell)

    def add_document_itmes(self, sheet: Worksheet, items: BaseModel, cell_itmes_number: int) -> int:
        """
        Вставляет строки в таблицу excel и возвращает смещение
        """
        merge_areas = []
        merge_items = []
        merge_items_name = None
        offset = 0
        #Заполняем список координат объедененных ячеек после строки с таблицы
        for mrg in sheet.merged_cells.ranges:
            start_col, start_row, end_col, end_row = range_boundaries(str(mrg))  # получаем границы объединённой области
            if start_row >= cell_itmes_number: 
                merge_areas.append(mrg)
            elif start_row >= cell_itmes_number-1 and end_row <= cell_itmes_number-1:
                merge_items.append(mrg)
                if start_col == 18:
                    merge_items_name = mrg
                

        #Сохраняем высоту строк
        row_heights = {}
        for row in range(cell_itmes_number, sheet.max_row):
            row_heights[row] = sheet.row_dimensions[row].height

        for merge_range in merge_areas:
            sheet.unmerge_cells(str(merge_range))

        #Сохраняем стили ячеек
        styles_source = []
        for cell in sheet[f'A{cell_itmes_number}':f'{get_column_letter(sheet.max_column)}{cell_itmes_number}'][0]:
            styles_source.append({
                'font': cell.font.copy(),
                'fill': cell.fill.copy(),
                'border': cell.border.copy(),
                'alignment': cell.alignment.copy()
         })
        
        offset = items.count()
        default_items_height = sheet.row_dimensions[cell_itmes_number].height

        #Добавляем строки и заполняем
        for i, item in enumerate(items.all()):
            number_of_row = cell_itmes_number + i
            sheet.insert_rows(number_of_row)

            for col_idx, style in enumerate(styles_source):
                target_cell = sheet.cell(row=number_of_row, column=col_idx + 1)
                target_cell.font = style['font']
                target_cell.fill = style['fill']
                target_cell.border = style['border']
                target_cell.alignment = style['alignment']

            if "items" in self.document_dict:
                for key, cell_ref in self.document_dict["items"].items():
                    if hasattr(item, key) and getattr(item, key):
                        value = str(getattr(item, key))
                        sheet[f'{cell_ref}{number_of_row}'] = value

                    if key == 'name':
                        if merge_items_name:
                            coords = range_boundaries(str(merge_items_name))
                            column_width = int(coords[2]) - int(coords[0])
                            sheet.row_dimensions[cell_itmes_number + i].height = self.calculate_row_height(value, target_cell.font, column_width)

            for area in merge_items:
                coords = range_boundaries(str(area))
                adjusted_area = f'{get_column_letter(coords[0])}{number_of_row}:{get_column_letter(coords[2])}{number_of_row}'
                sheet.merge_cells(adjusted_area)

        #Возвращаем высоту строк после добавления
        for row, height in row_heights.items():
            sheet.row_dimensions[row + offset].height = height

        #Соединяем зоны после добавления строк
        for area in merge_areas:
            coords = range_boundaries(str(area))
            adjusted_area = f'{get_column_letter(coords[0])}{coords[1]+offset}:{get_column_letter(coords[2])}{coords[3]+offset}'
            sheet.merge_cells(adjusted_area)

        return offset
    
    def calculate_row_height(self, text: str, font: Font, column_width: float) -> float:
        """
        Расчитывает выстоту строки
        """
        line_spacing = 1.5

        lines = text.split('\n')
        #print(f"{column_width}, {font.size}")
        approx_chars_per_line = math.floor(column_width / (font.size / 7))

        if not approx_chars_per_line:
            #print(text)
            approx_chars_per_line = 1

        num_lines = 0

        for line in lines:
            num_lines += math.ceil(len(line) / approx_chars_per_line)

        #print(f'{approx_chars_per_line}:{num_lines}:{len(lines[0])}')
        return font.size  * num_lines * line_spacing
    
    def row_height_from_content(self, sheet: Worksheet, value: str, cell_ref: str) -> None:
        """
        Изменяет высоту строки на основе контента
        """
        col_number, row_number = coordinate_from_string(cell_ref)
        row_number = int(row_number)
        new_height = self.calculate_row_height(value, sheet[cell_ref].font, self.get_merged_column_count(sheet, cell_ref))
        if not sheet.row_dimensions[row_number].height or new_height > sheet.row_dimensions[row_number].height:
            sheet.row_dimensions[row_number].height = new_height
        #print(f'{cell_ref}: {value}: {sheet.row_dimensions[row_number].height}')

    def get_merged_column_count(self, sheet: Worksheet, cell_ref: str) -> int:
        """
        Функция возвращает количество столбцов у объедененной ячейки
        """
        col_number, row_number = coordinate_from_string(cell_ref)
        col_number = column_index_from_string(col_number)
        row_number = int(row_number)

        for mrg in sheet.merged_cells.ranges:
            start_col, start_row, end_col, end_row = range_boundaries(str(mrg))  # получаем границы объединённой области
            if start_col <= col_number <= end_col and start_row <= row_number <= end_row:
                return end_col - start_col
            
        return 1

    def read_and_return_file(self, file_path: str) -> BytesIO:
        with open(file_path, 'rb') as f:
            data = f.read()
        buffer = BytesIO(data)
        buffer.seek(0)
        return buffer

    def toPDF_libre(self, file_path: str) -> BytesIO:

        base_dir = os.path.dirname(file_path)
        filename = os.path.basename(file_path).split('.')[0]
        out_file = os.path.join(base_dir, f'{filename}.pdf')

        #libreoffice_path = 'C:\\Program Files\\LibreOffice\\program\\soffice.exe'
        libreoffice_path = '/usr/bin/soffice'

        if not os.path.exists(file_path):
            print(f"Ошибка! Файл '{file_path}' не найден.")
        else:
            command = [
                libreoffice_path, '--headless',
                '--convert-to', 'pdf',
                '--outdir', base_dir,
                file_path,
            ]
            
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    raise Exception(result.stderr.decode())
                else:
                    return self.read_and_return_file(out_file)
            except Exception as err:
                print(f"Ошибка при преобразовании: {err}")

    """
    def toPDF_win32(self, file_name: str):
        file_path = 'C:\\Users\\reber\\PycharmProjects\\UPD\\src\\' + file_name
        pythoncom.CoInitialize()
        
        excel = None
        workbook = None
        
        try:
            # Открываем Excel
            excel = client.Dispatch("Excel.Application")
            excel.Visible = False  # Скрываем окно Excel

            # Открываем файл
            workbook = excel.Workbooks.Open(file_path)
            
            worksheet = workbook.Worksheets[0]

            #worksheet.HPageBreaks.Add(Before=worksheet.Rows(21)) Разрывы

            # Конвертируем в PDF
            out_file = file_path.replace('.xlsx', '.pdf')
            worksheet.ExportAsFixedFormat(0, out_file)

            return self.read_and_return_file(out_file)
            
        except Exception as e:
            print(f"Ошибка при конвертации: {e}")
            raise
            
        finally:
            if workbook:
                workbook.Close(SaveChanges=False)
            if excel:
                excel.Quit()
            pythoncom.CoUninitialize()

    def toPDF_spire(self, file_path: str):
        
        workbook = Workbook()
        workbook.LoadFromFile(file_path)
        for sheet in workbook.Worksheets:
            pageSetup = sheet.PageSetup
            pageSetup.TopMargin = 0.3
            pageSetup.BottomMargin = 0.3
            pageSetup.LeftMargin = 0.3
            pageSetup.RightMargin = 0.3

        workbook.ConverterSetting.SheetFitToPage = True
        
        out_file = file_path.replace('.xlsx', '.pdf')

        workbook.SaveToFile(out_file, FileFormat.PDF)
        workbook.Dispose()

        self.read_and_return_file(out_file)
    """        