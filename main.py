# from konwertuj_pdf import *

import zipfile
import os
import datetime as dt
import time


def main():
    input_list = []

    input_count = 0

    while True:
        
        input_count = len(os.listdir("./Input"))
        if input_count > 0:
            input_list = os.listdir("./Input")
            for f in input_list:
                time.sleep(5)
                print("dodano plik", f, "o", dt.datetime.now())           
                file_path = f"./Input/{f}"
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall("./Pliki")
                except:
                    print("cos poszło nie tak!!!")

                os.remove(f"./Input/{f}")


    





if __name__ == '__main__':
    main()