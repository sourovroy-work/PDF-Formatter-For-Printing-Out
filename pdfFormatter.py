import os
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileMerger

RAW_PATH = "./RawPDFs/*.pdf"
BLANK_PATH = "./BlankPDF/blank.pdf"
MERGED_FOLDER = "MergedPDFs"

pdfs = glob(RAW_PATH)
merger = PdfFileMerger()
for pdf in pdfs:
    merger.append(pdf)
    pdfReader = PdfFileReader(open(pdf, 'rb'))
    if pdfReader.numPages%2:
        merger.append(BLANK_PATH)
        
if not os.path.exists(MERGED_FOLDER):
    os.makedirs(MERGED_FOLDER)

merger.write(MERGED_FOLDER + "/result.pdf")
merger.close()
print("============================")
print("Operation Successful!!!\nDestination PATH: " + MERGED_FOLDER)
print("============================")
