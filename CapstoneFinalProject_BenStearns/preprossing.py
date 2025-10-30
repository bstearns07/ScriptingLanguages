########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: to enhance images so ocular recognition can read text more accurately
#######################################################################################################################

import cv2          #
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh