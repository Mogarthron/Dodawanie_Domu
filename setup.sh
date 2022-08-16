#!/bin/bash

apt update -y
apt -y install git python3-pip tesseract-ocr

git clone https://github.com/Mogarthron/Dodawanie_Domu.git

pip3 install -r ./Dodawanie_Domu/requirements.txt

mkdir Dodawanie_Domu/Input Dodawanie_Domu/Output Dodawanie_Domu/Pliki

which tesseract > Dodawanie_Domu/tes_path

