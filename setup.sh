#!/bin/bash

apt update -y
apt -y install git python3-pip tesseract-ocr
which tesseract > tes_path
git clone https://github.com/Mogarthron/Dodawanie_Domu.git

pip3 install -r ./Dodawanie_Domu/requirements.txt

mkdir Dodawanie_Domu/Input Dodawanie_Domu/Output Dodawanie_Domu/Pliki

