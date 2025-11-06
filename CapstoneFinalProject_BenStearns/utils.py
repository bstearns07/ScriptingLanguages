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