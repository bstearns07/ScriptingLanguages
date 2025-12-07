######################################################################################################################
# Project...............: Yugioh Card Library
# Author................: Ben Stearns
# Date..................: 12-4-25
# Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# File Description......: defines functions for extracting a card's attribute through best-match scenario
#######################################################################################################################

import os
import numpy as np
from PIL import Image
from YugiohCardDigitizer.preprocessing.preprocess_attribute import preprocess_attr_for_match


#######################################################################################################################
# Function that attempts to match a scanned card's attribute with base images in the "attributes" folder
# Parameters: the cropped attribute image and directory containing template images to compare
# Returns: the best match found
#######################################################################################################################
def classify_attribute(cropped_attr_img, template_dir="attributes"):
    """Classify attribute icon using normalized correlation instead of histogram distance."""
    # Preprocess the cropped icon exactly like the templates for better matching
    img = preprocess_attr_for_match(cropped_attr_img)
    img_arr = np.array(img, dtype=np.float32)
    img_arr = (img_arr - img_arr.mean()) / (img_arr.std() + 1e-6)

    # define variables to store the best matching label and matching score found
    best_match = None
    best_score = -1.0

    for filename in os.listdir(template_dir):
        if not filename.lower().endswith(".png"):
            continue

        label = filename.split(".")[0].upper()
        template = Image.open(os.path.join(template_dir, filename))
        template = preprocess_attr_for_match(template)
        template_arr = np.array(template, dtype=np.float32)
        template_arr = (template_arr - template_arr.mean()) / (template_arr.std() + 1e-6)

        # normalized cross-correlation
        score = np.mean(img_arr * template_arr)

        if score > best_score:
            best_score = score
            best_match = label

    return best_match