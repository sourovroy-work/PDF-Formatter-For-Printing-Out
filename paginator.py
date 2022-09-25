import os

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def create_page(num, tmp):
    c = canvas.Canvas(tmp)
    for i in range(1, num + 1):
        c.drawString((210 // 2) * mm, (4) * mm, "Page " + str(i))
        c.showPage()
    c.save()


def add_page_numbers(input_path, output_path):
    """
    Add page numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    """
    tmp = "__tmp.pdf"

    writer = PdfWriter()
    with open(input_path, "rb") as f:
        reader = PdfReader(f)
        n = len(reader.pages)
        
        create_page(n, tmp)

        with open(tmp, "rb") as ftmp:
            number_pdf = PdfReader(ftmp)
            for p in range(n):
                page = reader.pages[p]
                number_layer = number_pdf.pages[p]
                page.merge_page(number_layer)
                writer.add_page(page)
                
            if len(writer.pages) > 0:
                with open(output_path, "wb") as f:
                    writer.write(f)
                    
        os.remove(tmp)


if __name__ == "__main__":
    add_page_numgers("destination.pdf", "output.pdf")

