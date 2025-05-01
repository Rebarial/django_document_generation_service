from abc import ABC, abstractmethod
import os
from io import BytesIO
from documents_сreating.models.base import BaseModel
from openpyxl.utils import range_boundaries, get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.drawing.image import Image as XLImage
from django.core.files.storage import default_storage
from typing import BinaryIO

class BaseExcelDocumentCreate(ABC):
    """
    Базовый класс для создания excel документов
    """

    def __init__(self, document_dict: dict, template_path: str):
        self.document_dict = document_dict
        self.template_path = template_path

    @abstractmethod
    def create_excel_document(self, document: BaseModel) -> BinaryIO:
        """
        Создает excel документ на основе шаблона и словаря заполнения
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
        offset = 0

        #Заполняем список координат объедененных ячеек после строки с таблицы
        for mrg in sheet.merged_cells.ranges:
            strt_col, start_row, end_col, end_row = range_boundaries(str(mrg))  # получаем границы объединённой области
            if start_row >= cell_itmes_number: 
                merge_areas.append(mrg)
            if start_row >= cell_itmes_number and end_row <= cell_itmes_number:
                merge_items.append(mrg) 

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
                        sheet[f'{cell_ref}{number_of_row}'] = str(getattr(item, key))

            for area in merge_items:
                coords = range_boundaries(str(area))
                adjusted_area = f'{get_column_letter(coords[0])}{coords[1]+i}:{get_column_letter(coords[2])}{coords[3]+i}'
                sheet.merge_cells(adjusted_area)

        #Возвращаем высоту строк после добавления
        for row, height in row_heights.items():
            sheet.row_dimensions[row + offset].height = height

        #Присваеваем высоту добавленным строкам
        for i in range(1,offset):
            sheet.row_dimensions[cell_itmes_number + i].height = sheet.row_dimensions[cell_itmes_number].height

        #Соединяем зоны после добавления строк
        for area in merge_areas:
            coords = range_boundaries(str(area))
            adjusted_area = f'{get_column_letter(coords[0])}{coords[1]+offset}:{get_column_letter(coords[2])}{coords[3]+offset}'
            sheet.merge_cells(adjusted_area)

        return offset