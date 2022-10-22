import os
import SRC.paginator as paginator
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil

INPUT_PATH = "./INPUT/*.pdf"
OUTPUT_FOLDER = "OUTPUT"

BLANK_PATH = "./.cache/BLANK/blank.pdf"
TEMP_FOLDER = "./.cache/TEMP"
TEMP_PATH = TEMP_FOLDER + "/*.pdf"
DELETE_ME = "delete_me.txt"

LIMIT = 60

def clean(folder):
    if os.path.exists(folder):
        shutil.rmtree('./' + folder)
clean(TEMP_FOLDER)
clean(OUTPUT_FOLDER)

def create(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, DELETE_ME), 'w') as fp:
        pass
create(TEMP_FOLDER)
create(OUTPUT_FOLDER)

def add_numbering(pdfs):
    for pdf in pdfs:
        path = TEMP_FOLDER + "/" + pdf.rsplit(chr(92), 1)[-1]
        paginator.add_page_numbers(pdf, path)
add_numbering(glob(INPUT_PATH))

def merge(pdfs):
    merger = PdfFileMerger(strict=False)

    pdf_size=0
    pdf_id=1
    remain = False
    for index, pdf in enumerate(pdfs):
        try:
            pdfReader = PdfFileReader(open(pdf, 'rb'))
            pcount = pdfReader.getNumPages()
            
            merger.append(pdf)
            pdf_size+=pcount

            merger.append(BLANK_PATH)
            merger.append(BLANK_PATH)
            
            if pcount%2:
                merger.append(BLANK_PATH)
                pdf_size+=1

            remain = True
            if pdf_size>LIMIT:
                merger.write(OUTPUT_FOLDER + "/result-"+str(pdf_id)+".pdf")
                merger.close()
                merger = PdfFileMerger(strict=False)
                pdf_size=0
                pdf_id+=1
                remain = False
            print("PROCESSED => " + str(index+1) + "/" + str(len(pdfs)))
        except:
            print("ERROR!!! || PDF NAME: " + pdf)
        
    if remain:
        merger.write(OUTPUT_FOLDER + "/result-"+str(pdf_id)+".pdf")
    merger.close()

merge(glob(TEMP_PATH))

print("\nSUCCESSFUL!!!")
print("OUTPUT FOLDER: " + "./" + OUTPUT_FOLDER)
