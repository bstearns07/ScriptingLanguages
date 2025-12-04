######################################################################################################################
# Project...............: Yugioh Card Library
# Author................: Ben Stearns
# Date..................: 12-4-25
# Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# File Description......: defines a function to run the tesseract program on all image files in the samples directory
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


images_dir = "samples"  # represents the directory containing the images to scan

# defines a function that loops through all images in the scan directory and attempt to extra card data from them
def main():
    for file in os.listdir(images_dir):
        image_filepath = os.path.join(images_dir, file)     # defines the full filepath to the image
        processed_image = preprocess_image(image_filepath)  # prepare the image for tesseract and store
        text = extract_text(processed_image)                # extract all text from the card
        card = extract_card_info(text)                      # use the extracted text to create a card

        processed_image.save("tesseractImage.png")          # to save the processed image to debug what tesseract sees

        # print the results
        print("===Extracted Text===")
        print(text)
        print("===Image Information===")
        print(card.name, card.attack, card.defense, card.type, card.color)
        print(card.description)
        print()

if __name__ == "__main__":
    main()
