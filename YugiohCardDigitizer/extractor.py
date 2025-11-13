########################################################################################################################
# Title..............: Capstone Final Project - Ocular Recognition
# Author.............: Ben Stearns
# Date...............: 10-30-2025
# Purpose............: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: defines a function that uses pytesseract.image_to_string() to
#                      extract text from a preprocessed image
#######################################################################################################################

import pytesseract  # to allow the use of pytesseract.image_to_string() to extract text from an image

# defines a function that accepts an image and uses tesseract to extract text from it. Then returns the text
def extract_text(image):
    """
    Extracts text from an image using the Tesseract OCR engine.

    Parameters:
        image (PIL.Image.Image):
            The preprocessed image object to be analyzed.
            Typically returned from a preprocessing function that enhances contrast,
            resizes, or thresholds the image for better OCR accuracy.

    Returns:
        str: The text content detected in the image.
    """
    text = pytesseract.image_to_string(image, lang='eng')
    return text