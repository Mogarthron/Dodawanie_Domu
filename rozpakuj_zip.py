import zipfile
import os

with zipfile.ZipFile("./Input/21627.zip", 'r') as zip_ref:
    zip_ref.extractall("./Pliki")