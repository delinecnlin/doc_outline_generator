## utils/file_processor.py

import os
from typing import Union
from docx import Document
from PyPDF2 import PdfFileReader

class FileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_type = os.path.splitext(file_path)[1]

    def process_file(self) -> str:
        if self.file_type == '.docx':
            return self._process_word_file()
        elif self.file_type == '.pdf':
            return self._process_pdf_file()
        else:
            raise ValueError(f'Unsupported file type: {self.file_type}')

    def _process_word_file(self) -> str:
        doc = Document(self.file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])

    def _process_pdf_file(self) -> str:
        with open(self.file_path, 'rb') as file:
            pdf = PdfFileReader(file)
            return ' '.join([pdf.getPage(i).extractText() for i in range(pdf.getNumPages())])
