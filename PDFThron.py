from PDFNetPython3 import *

import os


with open("PDFThronLicence", "r") as f:
    LicenseKey = f.read()

PDFNet.Initialize(LicenseKey)


def RozdzielWarstwy(file_path, ImageSize = [5000,5000]) -> None:
    f_name = file_path.split('/')[-1].replace(".pdf", "")
    os.makedirs(f_name, exist_ok=True)
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
            fname = os.path.join(f_name,ocg.GetName() + ".png")
            pdfdraw.Export(page, fname)
        if "+Z1~" in ocg.GetName():
            ctx.ResetStates(False)
            ctx.SetState(ocg, True)
            fname = os.path.join(f_name,ocg.GetName() + ".png")
            pdfdraw.Export(page, fname)
        if ocg.GetName() == "0":
            ctx.ResetStates(False)
            ctx.SetState(ocg, True)
            fname = os.path.join(f_name,ocg.GetName() + ".png")
            pdfdraw.Export(page, fname)
        # else:
        #     ctx.ResetStates(False)
        #     ctx.SetState(ocg, True)
        #     fname = os.path.join(f_name,ocg.GetName() + ".png")
        #     pdfdraw.Export(page, fname)
            
       
    # Now draw content that is not part of any layer...
    # ctx.SetNonOCDrawing(True)
    # ctx.SetOCDrawMode(Context.e_NoOC)
    # pdfdraw.Export(page, os.path.join(f_name,"pdf_layers_non_oc.png"))