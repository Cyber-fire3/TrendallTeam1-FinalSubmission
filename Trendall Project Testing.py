
#PDF To Image Extraction Tool

"""from pdf2image import convert_from_path

pages = convert_from_path('RVP.pdf')

# Save each page as a JPEG file using Pillow

for i, page in enumerate(pages):
	page.save(f'PLATE_{i}.jpg', 'JPEG')
"""

#PDF To Image Extraction Tool

"""poppler_path = r"C:\Users\joshw\Downloads\JPEG-FOLDER\poppler-24.02.0\Library\bin"
pdf_path = r"C:\Users\joshw\Downloads\JPEG-FOLDER\RVP.pdf"

from pdf2image import convert_from_path
import os

pages = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)

saving_folder = r"C:\Users\joshw\Downloads\JPEG-FOLDER\IMAGES"
c = 1
for page in pages:
    img_name = f"img-{c}.jpeg"
    page.save(os.path.join(saving_folder, img_name), "JPEG")
    c += 1"""
    
#PDF To Image Extraction Tool

"""
# Store Pdf with convert_from_path function
images = convert_from_path('RVP.pdf')
 
for i in range(len(images)):
   
      # Save pages as images in the pdf
    images[i].save('page'+ str(i) +'.jpg', 'JPEG')"""




#Testing Text File Outputs From RVP.PDF as "Small.txt"

"""
text_file = open("Small.txt", "r")
lines = text_file.readlines()
print(lines)
"""
"""vases = []
text_file = open("Master-Test.txt", "r")
lines = text_file.readlines()

for line in lines:
    if "*1" in line:
        vases.append(line)
        #print(line)
text_file.close()
print(vases)"""


"""
test = ["Calyx-kraters (fragmentary) *242 Bari 3581, from Taranto. Actual ht. 17-2, diam. 25-2. PLATE 93 a"]
#print(test)
test1 = {"id": "PP-1-1", "Fabric": "Paestan", "Painter": "Dirce Group", "Provenance": "Bari 3581, from Taranto.", "Dimensions": "Actual ht. 17-2, diam. 25-2.", 
         "Publications": "abc", "Description": "def"}
print(test1)
# What chapter are you extracting from = 2 (x)
# What sub chapter are you extracting from = "The Dirce Group"
# []
# 
# 2 = THE SICILIAN FORERUNNERS 
# 2.1 = Dirce Group
# 2.2 = THE PRADO/FIENGA GROUP

#Chapter = input()
"""
"""# importing required modules
from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('TESTING.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[1]

# extracting text from page
text = page.extract_text()
print(text)"""


#Script To Extract Certain Pages From PDF
"""
from PyPDF2 import PdfReader, PdfWriter
#Extract certain pages from PDF#
file_name = 'RVP.pdf'
pages = (55, 57)
reader = PdfReader(file_name)
writer = PdfWriter()
page_range = range(pages[0], pages[1] + 1)

for page_num, page in enumerate(reader.pages, 1):
    if page_num in page_range:
        writer.add_page(page)

with open(f'{file_name}_page_{pages[0]}-{pages[1]}.pdf', 'wb') as out:
    writer.write(out)
"""


#--------------------------------------------------------------------------------------------------------------------------------------------#
#Image Extraction Code
"""
pdf = fitz.open("RVP.pdf")
counter = 1
for i in range(len(pdf)):
    page = pdf[i]
    images = page.get_images()
    for image in images:
        base_img = pdf.extract_image(image[0])
        image_data = base_img["image"]
        img = PIL.Image.open(io.BytesIO(image_data))
        extension = base_img["ext"]
        img.save(open(f"image{counter}.{extension}", "wb"))
        counter += 1
"""

#Testing Ways To Extract Physical Dimensions 
"""
newVase = 0
test_file = open('Small-Test.txt', 'r')
for line in test_file:
    if "Ht." in line:
        newVase += 1
    elif "ht. " in line:
        newVase += 1
    elif "Diam. " in line:
        newVase += 1
    elif "diam. " in line:
        newVase += 1

"""


