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

def extract_contact_info(text):
    # Normalize OCR quirks
    cleaned = text.replace("—", "-").replace(":", "-").replace("#", "")

    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', cleaned)
    phones = re.findall(r'\(?\d{2,3}\)?[-.\s]?\d{2,3}[-.\s]?\d{3,4}', cleaned)
    names = [line.strip() for line in cleaned.split('\n')
             if line.strip() and line[0].isupper() and len(line.split()) <= 3]

    return {
        'emails': emails,
        'phones': phones,
        'names': names,
    }