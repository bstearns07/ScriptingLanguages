
"""
description.py
--------------
Functions for cleaning OCR text extracted from a Yu-Gi-Oh card's description box.
"""

import re


def clean_description(text: str) -> str:
    """
    Cleans raw OCR text from the description box.

    Parameters
    ----------
    text : str
        Raw OCR text extracted by Tesseract.

    Returns
    -------
    str
        Cleaned, human-readable description string.
    """

    if not text:
        return ""

    # --- Remove isolated capital letters (OCR noise from ATK/DEF borders) ---
    # Example: "This is a test A text B" → "This is a test text"
    cleaned = re.sub(r'\b[A-Z]{1,2}\b', '', text)

    # --- Remove stray OCR symbols often misinterpreted by Tesseract ---
    cleaned = re.sub(r'[\|\=\>\<\&]', '', cleaned)

    # --- Replace multiple spaces with a single space ---
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)

    # Trim leading/trailing spaces
    return cleaned.strip()
