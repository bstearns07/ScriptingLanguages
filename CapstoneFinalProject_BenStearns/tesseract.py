########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description..: defines the function to run the tesseract program
#######################################################################################################################
# REQUIRED: Download tesseract here => https://github.com/UB-Mannheim/tesseract/wiki
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# imports
import os

from preprossing import preprocess_image
from extractor import extract_text
from utils import extract_contact_info
import cv2          # to allow for preprocessing of images to prepare for OCR

images_dir = "samples"

def main():
    for file in os.listdir(images_dir):
        image_filepath = os.path.join(images_dir, file)
        processed_image = preprocess_image(image_filepath)
        text = extract_text(processed_image)
        info = extract_contact_info(text)

        cv2.imwrite("../debug_processed.jpg", processed_image)

        print("===Extracted Text===")
        print(text)
        print("===Image Information===")
        print(info)
        print()

if __name__ == "__main__":
    main()

