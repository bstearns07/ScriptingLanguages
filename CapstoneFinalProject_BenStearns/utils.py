########################################################################################################################
# Title.............: Capstone Final Project - Ocular Recognition
# Author............: Ben Stearns
# Date..............: 10-30-2025
# Purpose...........: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description..: uses regex pattern for find specific data types from an image's extracted text
#######################################################################################################################

# imports
import re

def extract_contact_info(text):
    emails = re.findall(r'\S+@\S+', text)
    phones = re.findall(r'\d{3}[-.\s]\d{3}[-.\s]\d{4}', text)
    names = [line for line in text.split('n') if line.istitle() and len(line.split()) <= 3]
    return {
        'emails': emails,
        'phones': phones,
        'names': names,
    }