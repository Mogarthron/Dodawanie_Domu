import fitz

# print(fitz.__doc__)
base = "./Dane/"
path = "1-SD-02_konA4.pdf"
doc = fitz.open(base + path)
# page = doc.load_page(0)
# print(page.get_text("text"))
# annot = page.annots()

# for an in annot:
#     print(an ,an.get_textbox("text"), len(an.get_textbox("text")))


zoom_x = 8.0  # horizontal zoom
zoom_y = 8.0  # vertical zoom
mat = fitz.Matrix(zoom_x, zoom_y)
for page in doc:  # iterate through the pages
    pix = page.get_pixmap(matrix=mat)  # render page to an image
    pix.save(f"{path[:-4]}.png")  # store image as a PNG
    