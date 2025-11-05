########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description..: uses tesseract library to extract text from a preprocessed image
#######################################################################################################################
from PIL import Image
import pytesseract

def extract_text(image):
    text = pytesseract.image_to_string(Image.fromarray(image), lang='eng')
    return text