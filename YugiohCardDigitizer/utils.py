# ######################################################################################################################
# # Project...............: Yugioh Card Library
# # Author................: Ben Stearns
# # Date..................: 12-4-25
# # Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# # File Description......: defines utility functions for extracting Yugioh card data from an image
# #######################################################################################################################
#
# # imports
# import re           # to allow the use of regular expression pattern matching
# import numpy as np  # used to manipulate OpenCV image arrays
#
# from Yugioh_Card import YugiohCard
#
# def extract_card_info(text):
#     """
#     Extracts key Yu-Gi-Oh! card information from OCR's text and returns a YugiohCard object.
#
#     Parameters:
#         text
#             The text that was extracted from a card image by tesseract
#
#     Returns:
#         YugiohCard: a card representing the extracted text's data
#     """
#     # Normalize OCR quirks (common text issues)
#     cleaned = (
#         text.replace("—", "-")  # replace em-dashes with a normal dash
#         .replace(":", "/")      # replace colons with forward slash
#         .replace("#", "")       # remove hash symbols
#         .replace("0f", "of")    # common OCR typo
#         .replace("0", "o")      # fix OCR'd zeros as o's in text
#         .strip()                # remove starting and ending whitespace
#     )
#
#     # Match patterns even with minor OCR inconsistencies and clean up the results
#     name_match = re.search(r"([A-Z][A-Za-z\s'\-]+)", cleaned)
#     atk_match = re.search(r"ATK\s*[/\-]?\s*(\d{3,5})", cleaned, re.IGNORECASE)
#     def_match = re.search(r"DEF\s*[/\-]?\s*(\d{3,5})", cleaned, re.IGNORECASE)
#     type_match = re.search(r"\[(.*?)\]", cleaned)  # e.g. [Dragon/Effect]
#     desc_match = re.search(r"(?s)(?:This|A|The).*?(?=ATK|DEF|$)", cleaned)
#     color_match = re.search(r"Attribute\s*[:\-]?\s*(\w+)", cleaned, re.IGNORECASE)
#
#     # extract data from the pattern matching results
#     name = name_match.group(1).strip() if name_match else "Unknown Card"
#     description = desc_match.group(0).strip() if desc_match else "No description available."
#     attack = int(atk_match.group(1)) if atk_match else "NA"
#     defense = int(def_match.group(1)) if def_match else "NA"
#     type_ = type_match.group(1).strip() if type_match else "Unknown Type"
#     color = color_match.group(1).capitalize() if color_match else "Unknown"
#
#     # return the results as a card object
#     return YugiohCard(name, description, attack, defense, type_, color)
#
# # defines a function that takes the four corners of a card and returns them in a consistent layout
# def order_points(pts):
#     rect = np.zeros((4, 2), dtype = "float32")  # creates an empty container for the ordered points
#     s = pts.sum(axis = 1)
#     rect[0] = pts[np.argmin(s)]
#     rect[2] = pts[np.argmax(s)]
#     diff = np.diff(pts, axis = 1)
#     rect[1] = pts[np.argmin(diff)]
#     rect[3] = pts[np.argmax(diff)]
#     return rect
