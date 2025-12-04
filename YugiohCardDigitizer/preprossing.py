######################################################################################################################
# Project...............: Yugioh Card Library
# Author................: Ben Stearns
# Date..................: 12-4-25
# Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# File Description......: to enhance images so ocular recognition can read text more accurately
#######################################################################################################################

from PIL import Image, ImageEnhance, ImageOps, ImageFilter  # for image manipulation

def binarize(image, threshold=150):
    return image.point(lambda x: 0 if x < threshold else 255, '1')

def preprocess_image(image_path):
    # Load image
    image = Image.open(image_path)

    # Convert to grayscale (Tesseract prefers grayscale over color)
    gray = image.convert("L")

    # gray = gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)
    # gray = binarize(gray, threshold=140)  # tweak threshold for best results
    # gray = gray.filter(ImageFilter.MedianFilter(size=3))
    # gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=1))

    # Auto-adjust contrast and brightness to normalize lighting
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(2.0)
    gray = ImageEnhance.Brightness(gray).enhance(1.2)

    # Sharpen text edges slightly
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    return gray
