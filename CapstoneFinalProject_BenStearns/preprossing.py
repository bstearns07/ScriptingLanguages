########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: to enhance images so ocular recognition can read text more accurately
#######################################################################################################################

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np

def preprocess_image(image_path):
    # Load image
    image = Image.open(image_path)

    # Convert to grayscale
    gray = image.convert("L")

    # Resize to improve OCR accuracy
    scale = 1.5
    new_size = (int(gray.width * scale), int(gray.height * scale))
    gray = gray.resize(new_size, Image.LANCZOS)

    # Increase contrast and brightness slightly
    enhancer_contrast = ImageEnhance.Contrast(gray)
    gray = enhancer_contrast.enhance(1.5)  # contrast factor

    enhancer_brightness = ImageEnhance.Brightness(gray)
    gray = enhancer_brightness.enhance(1.1)  # brightness factor

    # Convert to NumPy for thresholding (like cv2 adaptive threshold)
    np_img = np.array(gray)

    # Simple adaptive threshold approximation
    mean = np_img.mean()
    binary = np.where(np_img > mean - 15, 255, 0).astype(np.uint8)

    # Back to Pillow for saving/processing
    processed = Image.fromarray(binary)

    # Optional: denoise slightly
    processed = processed.filter(ImageFilter.MedianFilter(size=3))

    return processed
