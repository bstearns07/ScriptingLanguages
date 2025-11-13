########################################################################################################################
# Title..............: Capstone Final Project - Ocular Recognition
# Author.............: Ben Stearns
# Date...............: 10-30-2025
# Purpose............: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: uses regex patterns for find specific data types from an image's extracted text
#######################################################################################################################

# imports
import re   # to allow the use of regular expression pattern matching

import cv2
import numpy as np

from Yugioh_Card import YugiohCard

def extract_card_info(text):
    """
    Extracts key Yu-Gi-Oh! card information from OCR's text and returns a YugiohCard object.

    Parameters:
        text
            The text that was extracted from a card image by tesseract

    Returns:
        YugiohCard: a card representing the extracted text's data
    """
    # Normalize OCR quirks (common text issues)
    cleaned = (
        text.replace("—", "-")
        .replace(":", "/")
        .replace("#", "")
        .replace("0f", "of")  # common OCR typo
        .replace("0", "o")    # fix OCR'd zeros as o's in text
        .strip()
    )

    # Match patterns even with minor OCR inconsistencies
    name_match = re.search(r"([A-Z][A-Za-z\s'\-]+)", cleaned)
    atk_match = re.search(r"ATK\s*[/\-]?\s*(\d{3,5})", cleaned, re.IGNORECASE)
    def_match = re.search(r"DEF\s*[/\-]?\s*(\d{3,5})", cleaned, re.IGNORECASE)
    type_match = re.search(r"\[(.*?)\]", cleaned)  # e.g. [Dragon/Effect]
    desc_match = re.search(r"(?s)(?:This|A|The).*?(?=ATK|DEF|$)", cleaned)
    color_match = re.search(r"Attribute\s*[:\-]?\s*(\w+)", cleaned, re.IGNORECASE)

    name = name_match.group(1).strip() if name_match else "Unknown Card"
    description = desc_match.group(0).strip() if desc_match else "No description available."
    attack = int(atk_match.group(1)) if atk_match else "NA"
    defense = int(def_match.group(1)) if def_match else "NA"
    type_ = type_match.group(1).strip() if type_match else "Unknown Type"
    color = color_match.group(1).capitalize() if color_match else "Unknown"

    return YugiohCard(name, description, attack, defense, type_, color)

def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped