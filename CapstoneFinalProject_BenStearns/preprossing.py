########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: to enhance images so ocular recognition can read text more accurately
#######################################################################################################################

from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def preprocess_image(image_path):
    # Load image
    image = Image.open(image_path)

    # Convert to grayscale (Tesseract prefers grayscale over color)
    gray = image.convert("L")

    # Auto-adjust contrast and brightness to normalize lighting
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(2.0)
    gray = ImageEnhance.Brightness(gray).enhance(1.2)

    # Sharpen text edges slightly
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Optional: slight denoise (only if you have lots of speckles)
    # gray = gray.filter(ImageFilter.MedianFilter(size=3))

    return gray
