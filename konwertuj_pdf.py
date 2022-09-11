import fitz
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

import numpy as np
import os


with open("tes_path", "r") as f:
    tes_path = f.read()


pytesseract.pytesseract.tesseract_cmd = tes_path


class Zestawinie_Okien:
    NUMER_STRONY = 0
    def __init__(self, pdf_page) -> None:

        self.Zestawienie_Okien = False
        self.text = ""

        if "FENSTER ZUSAMMENSTELLUNG" in self.text:
            self.Zestawienie_Okien = True
            self.text = pdf_page.get_text()
    

class PDF_Do_XXX:
    def __init__(self, path_to_pdf, rozszerzenie_obrazu="png") -> None:
        self.__path_to_pdf = path_to_pdf
        self.__rozszerzenie_obrazu = rozszerzenie_obrazu
        self.__doc = fitz.open(path_to_pdf)
        self.Ilosc_Ston = self.__doc.page_count
        self.toc = self.__doc.get_toc() #Table of content
        self.Zawarosc_stron = [self.__doc.load_page(x) for x in range(self.__doc.page_count)]

        # if self.Ilosc_Ston > 1:
          
        #     for o in self.Zawarosc_stron:
        #         if o.Zestawienie_Okien:
        #             self.Zawarosc_stron = o.text

        if self.Ilosc_Ston == 1 and "_Pm_50_Nowy" in path_to_pdf:
            #wyszukanie okien przy ścianach
            Okna_Przy_Scianach = self.Konwersja_pdf_png(zoom=(9,9))
            #dodać tworznie pliku textowego z oknami o włściwej mazwie
            #określenie typu ściany (kolankowa, ogionowa, )
            print(Okna_Przy_Scianach[1])

        if self.Ilosc_Ston == 1 and "_kon" in path_to_pdf:

            print("Rysunek konstrukcji")
        
        if self.Ilosc_Ston == 1 and "_zgk" in path_to_pdf:

            print("Rysunek GK")


    def Konwersja_pdf_png(self, strona=0, zoom=(8,8), FILTR=200):
        
        zoom_x = zoom[0]  #powiekszenie strony na osi x
        zoom_y = zoom[1]  #powiekszenie strony na osi y

        page = self.__doc.load_page(strona)       
        mat = fitz.Matrix(zoom_x, zoom_y) 

        pix = page.get_pixmap(matrix=mat)  #bitowa reprezentacja strony pdf
        nazwa_pliku = self.__path_to_pdf.split('/')[-1][:-4]
        path_png = f"./Output/{nazwa_pliku}.{self.__rozszerzenie_obrazu}"

        im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples) #utworzenie templatki na png
        im = im.filter(ImageFilter.MedianFilter()) 
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(5)
        im = im.convert('L') #L = R * 299/1000 + G * 587/1000 + B * 114/1000
        im.save(path_png) # zapis pliku png
        data = np.array(im)
    
        mask = data > FILTR
        
        data[mask] = 0 #zamiana wszytkich pixeli spełniających warunek na czarny 
        new_im = Image.fromarray(data)
        # new_im.show()

        return new_im, nazwa_pliku


    def Wykryj_text_na_png(self, image, im_name, rotate=False):   

        text = pytesseract.image_to_string(image)
        text = text.strip()
        with open(f"./Output/{im_name}_raw.txt", "w", encoding='utf-8') as f:
            f.write(text)




def Wyszukaj_otwory(text:str, znacznik_otworu:str):
    """
    znacznik_otworu = "w" lub "d" od window, door
    """
    w = 0  #znacznik zapisu tekstu do zmiennej s
    i = 0  #iterator długosci tekstu 

    s = ""
    for t in enumerate(text):
        if t[1] == znacznik_otworu:
            w = 1  
            i = 1 

        if w == 1:
            s += t[1] 

        if t[1] == ")":
            w = 0
        
        if i > 0:
            i += 1
        
        if i > 15:
            w = 0

        
    s = s.replace(chr(162), "(").replace(chr(32), "")

    w = 0  #znacznik zapisu tekstu do zmiennej wymiary_otworu
    i = 0  #iterator długosci tekstu

    wymiary_otworu = ""

    for x in range(1, len(s)):
        if s[x-1]+s[x] == f"{znacznik_otworu}(":
            w = 1
            i = 1

        if w == 1:
            wymiary_otworu += s[x] 
        
        if s[x] == ")":
            w = 0

    wymiary_otworu = wymiary_otworu.split(")(")

    for o in range(len(wymiary_otworu)):
        wymiary_otworu[o] = wymiary_otworu[o].replace("(", "")        
        wymiary_otworu[o] = wymiary_otworu[o].replace(")", "")
        

    return wymiary_otworu


def Konwersja_pdf_png(path_to_pdf, zoom=(8,8), FILTR = 200):
    doc = fitz.open(path_to_pdf)
    print(doc.page_count)
    
    page = doc.load_page(0)       

    zoom_x = zoom[0]  #powiekszenie strony na osi x
    zoom_y = zoom[1]  #powiekszenie strony na osi y

    mat = fitz.Matrix(zoom_x, zoom_y) 

    pix = page.get_pixmap(matrix=mat)  #bitowa reprezentacja strony pdf
    nazwa_pliku = path_to_pdf.split('/')[-1][:-4]
    path_png = f"./Output/{nazwa_pliku}.png"

    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples) #utworzenie templatki na png
    im = im.filter(ImageFilter.MedianFilter()) 
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(5)
    im = im.convert('L') #L = R * 299/1000 + G * 587/1000 + B * 114/1000
    im.save(path_png) # zapis pliku png
    data = np.array(im)
  
    mask = data > FILTR
    
    data[mask] = 0 #zamiana wszytkich pixeli spełniających warunek na czarny 
    new_im = Image.fromarray(data)
    # new_im.show()
    

    return new_im, nazwa_pliku


def Wykryj_text_na_png(image, im_name, rotate=False):   

    text = pytesseract.image_to_string(image)
    text = text.strip()
    with open(f"./Output/{im_name}_raw.txt", "w", encoding='utf-8') as f:
        f.write(text)







