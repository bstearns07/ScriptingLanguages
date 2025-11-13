########################################################################################################################
# Title..............: Capstone Final Project - Ocular Recognition
# Author.............: Ben Stearns
# Date...............: 10-30-2025
# Purpose............: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: defines a function to run the tesseract program on all image files
#######################################################################################################################
# REQUIRED: Download tesseract here => https://github.com/UB-Mannheim/tesseract/wiki
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# python.org/downloads/release/python-3127
# imports
import os

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from preprossing import preprocess_image    # for use of the preprocess_image() function
from extractor import extract_text          # for use of the extract_text() function
from utils import extract_card_info      # for use of the extract_contact_info() function


images_dir = "samples"

def main():
    for file in os.listdir(images_dir):
        image_filepath = os.path.join(images_dir, file)
        processed_image = preprocess_image(image_filepath)
        text = extract_text(processed_image)
        card = extract_card_info(text)

        processed_image.save("tesseractImage.png")

        print("===Extracted Text===")
        print(text)
        print("===Image Information===")
        print(card.name, card.attack, card.defense, card.type, card.color)
        print(card.description)
        print()

if __name__ == "__main__":
    main()
