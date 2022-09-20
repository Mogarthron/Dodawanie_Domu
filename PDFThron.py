from PDFNetPython3 import *
from PIL import  Image

import os


with open("PDFThronLicence", "r") as f:
    LicenseKey = f.read()

PDFNet.Initialize(LicenseKey)


def RozdzielWarstwy(file_path, folder_zapisu, ImageSize = [5000,5000]) -> None:
    f_name = file_path.split('/')[-1].replace(".pdf", "")
    os.makedirs(folder_zapisu, exist_ok=True)
    doc = PDFDoc(file_path)
    page = doc.GetPage(1)
    init_cfg = doc.GetOCGConfig()
    ctx = Context(init_cfg)
    pdfdraw = PDFDraw()
    pdfdraw.SetImageSize(ImageSize[0], ImageSize[1])
    pdfdraw.SetOCGContext(ctx)  # Render the page using the given OCG context.
    # Disable drawing of content that is not optional (i.e. is not part of any layer).
    ctx.SetNonOCDrawing(False)
    # Now render each layer in the input document to a separate image.
    ocgs = doc.GetOCGs()    # Get the array of all OCGs in the document.
    for i in range(ocgs.Size()):
        ocg = Group(ocgs.GetAt(i))
        if "^Z1~" in ocg.GetName():
            ctx.ResetStates(False)
            ctx.SetState(ocg, True)
            fname = os.path.join(folder_zapisu, ocg.GetName() + ".png")
            pdfdraw.Export(page, fname)
        if "+Z1~" in ocg.GetName():
            ctx.ResetStates(False)
            ctx.SetState(ocg, True)
            fname = os.path.join(folder_zapisu, ocg.GetName() + ".png")
            pdfdraw.Export(page, fname)
        if ocg.GetName() == "0":
            ctx.ResetStates(False)
            ctx.SetState(ocg, True)
            fname = os.path.join(folder_zapisu, ocg.GetName() + ".png")
            pdfdraw.Export(page, fname)
        # else:
        #     ctx.ResetStates(False)
        #     ctx.SetState(ocg, True)
        #     fname = os.path.join(f_name,ocg.GetName() + ".png")
        #     pdfdraw.Export(page, fname)
            
def ScalObrazy(obr1, obr2, filename, warstwa) -> None:
    """
    warstwa 1 = (0,5000, width, 10000)
    warstwa -1 = (0, 0, width, 5000)
    """
    background = Image.open(obr1)
    overlay = Image.open(obr2)
    background = background.convert("L")
    overlay = overlay.convert("L")
    img = Image.blend(background, overlay, 0.5)
    width, height = img.size
    # print(width, height)
    if warstwa == 1:
        new_img = img.crop((0,5000, width, 10000))
    if warstwa == -1:
        new_img = img.crop((0,0, width, 5000))
    # new_img.show()
    new_img.save(f"{filename}.png","PNG")   



def main():
  

    base_path = "./Pliki"

    for folder in os.listdir(base_path):
        _osb = [x for x in os.listdir(os.path.join(base_path, folder)) if x.endswith(".pdf") if "_osb" in x][:5]
        _zgk = [x for x in os.listdir(os.path.join(base_path, folder)) if x.endswith(".pdf") if "_zgk" in x][:5]


        for i in _osb:
     
            file_path = os.path.join(base_path, folder, i)
            folder_zapisu=f"./Output/{folder}/{i[:-4]}"
            RozdzielWarstwy(file_path=file_path, folder_zapisu=folder_zapisu, ImageSize=[10000,10000])
            print("Rozdzielono warstwy {i}")

            # lista_warstw = os.listdir(folder_zapisu.split('/')[-1].replace(".pdf", ""))
            # print(lista_warstw)
            # pierwsza_warstwa = [x for x in lista_warstw if "+Z1~" in x]
            # druga_warstwa = [x for x in lista_warstw if "^Z1~" in x]

            # if len(pierwsza_warstwa) > 0:
            #     obr1 = f"./{i[:-3]}/0.png"
            #     obr2 = f"./{i[:-3]}/{pierwsza_warstwa[0]}"

            #     ScalObrazy(obr1, obr2, f"{filename.split('/')[-1].replace('.pdf', '')}_1", 1)

            # if len(druga_warstwa) > 0:
            #     obr1 = f"./{i[:-3]}/0.png"
            #     obr2 = f"./{i[:-3]}/{druga_warstwa[0]}"

            #     ScalObrazy(obr1, obr2, f"{filename.split('/')[-1].replace('.pdf', '')}_-1", -1)




if __name__ == '__main__':
    main()
    