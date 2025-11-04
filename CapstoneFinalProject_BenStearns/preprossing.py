########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: to enhance images so ocular recognition can read text more accurately
#######################################################################################################################

# imports
import cv2          # to allow for preprocessing of images to prepare for OCR

def preprocess_image(image_path):
    # image = cv2.imread(image_path)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # return gray
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize (helps Tesseract on small fonts)
    scale_percent = 150  # 150% of original size
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)

    # Apply contrast and brightness adjustment (normalize)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=10)

    # Use adaptive thresholding for uneven lighting
    adaptive = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,  # blockSize (odd number)
        10  # constant subtracted from mean
    )

    # Optional: slight noise reduction
    denoised = cv2.medianBlur(adaptive, 3)

    return denoised