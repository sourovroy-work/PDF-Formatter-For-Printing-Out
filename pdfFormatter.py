import os
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileMerger

RAW_PATH = "./RawPDFs/*.pdf"
BLANK_PATH = "./BlankPDF/blank.pdf"
MERGED_FOLDER = "MergedPDFs"
LIMIT = 100

pdfs = glob(RAW_PATH)
merger = PdfFileMerger(strict=False)

if not os.path.exists(MERGED_FOLDER):
    os.makedirs(MERGED_FOLDER)

pdf_size=0
pdf_id=1
for pdf in pdfs:
    pdfReader = PdfFileReader(open(pdf, 'rb'))
    pcount = pdfReader.getNumPages()
    
    merger.append(pdf)
    pdf_size+=pcount
    
    if pcount%2:
        merger.append(BLANK_PATH)
        pdf_size+=1

    remain = True
    if pdf_size>LIMIT:
        merger.write(MERGED_FOLDER + "/result-"+str(pdf_id)+".pdf")
        merger.close()
        merger = PdfFileMerger(strict=False)
        pdf_size=0
        pdf_id+=1
        remain = False 
    
if remain:
    merger.write(MERGED_FOLDER + "/result-"+str(pdf_id)+".pdf")
merger.close()

print("============================")
print("Operation Successful!!!\nDestination PATH: " + MERGED_FOLDER)
print("============================")
