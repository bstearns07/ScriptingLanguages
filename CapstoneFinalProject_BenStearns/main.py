########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description..:
#######################################################################################################################
# REQUIRED: Download tesseract here => https://github.com/UB-Mannheim/tesseract/wiki
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# imports
import os

from preprossing import preprocess_image
from extractor import extract_text
from utils import extract_contact_info

def main():
    for file in os.listdir('samples'):
        processed_image = preprocess_image(file)
        text = extract_text(processed_image)
        info = extract_contact_info(processed_image)

        print("===Extracted Text===")
        print(text)
        print("===Image Information===")
        print(info)

if __name__ == "__main__":
    main()

