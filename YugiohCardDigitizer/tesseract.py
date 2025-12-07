######################################################################################################################
# Project...............: Yugioh Card Library
# Author................: Ben Stearns
# Date..................: 12-4-25
# Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# File Description......: defines functions that processes a Yugioh card into data that can be saved to the database
#######################################################################################################################

# imports
from PIL import Image, ImageOps, ImageFilter, ImageEnhance  # for image manipulation
import pytesseract                              # for ocular recognition functionality
import re                                       # for pattern matching text extracted from cards
import numpy as np
import difflib
import os

# define a list of all monster types for matching
KNOWN_TYPES = [
    "AQUA", "BEAST", "BEAST-WARRIOR", "CREATOR GOD", "CYBERSE", "DINOSAUR",
    "DIVINE-BEAST", "DRAGON", "FAIRY", "FIEND", "FISH", "INSECT", "MACHINE",
    "PLANT", "PSYCHIC", "PYRO", "REPTILE", "ROCK", "SEA SERPENT",
    "SPELLCASTER", "THUNDER", "WARRIOR", "WINGED BEAST", "WYRM", "ZOMBIE"
]
# Common OCR corrections for Yu-Gi-Oh monster types
COMMON_FIXES = {"0": "O","1": "I","5": "S","6": "G","8": "B","4": "A","|": "I","{": "[","}": "]",}

#######################################################################################################################
# Function that cleans the raw string data extracted from a card's monster_type data into a usable form
# Parameters: the text extracted regarding the card's monster_type information
# Returns: extracted text that's been sanitized, and formatted
#######################################################################################################################
def clean_raw_type(text):
    """Normalize raw OCR output before matching."""
    # if the string came up empty, return an empty string
    if not text:
        return ""
    # strip whitespace and cast to uppercase
    text_cleaned = text.upper().strip()
    # Loop through every character in the string and replace with a corrected character if it's considered a common fix
    # otherwise return the character unchanged. Join all the characters back into a new string
    text_cleaned = "".join(COMMON_FIXES.get(c, c) for c in text_cleaned)
    # Remove anything not A–Z, space, bracket, or dash
    text_cleaned = re.sub(r"[^A-Z\[\]\- ]", "", text_cleaned)
    # Remove brackets for to make matching the text to an entry in KNOWN_TYPES easier
    text_cleaned = text_cleaned.replace("[", "").replace("]", "").strip()
    return text_cleaned

#######################################################################################################################
# Function that replaces text misreads by OCR with fixed version in a consistent format
# Parameters: the text that needs fixed
# Returns: the corrected version of the text
#######################################################################################################################
def fix_atkdef_labels(text):
    t = text.upper()
    # fix common misreads
    t = t.replace("ALK", "ATK")
    t = t.replace("DFF", "DEF")
    t = t.replace("DE8", "DEF")
    t = t.replace("DEF/", "DEF:")
    t = t.replace("ATK/", "ATK:")
    t = t.replace(" ", "")        # remove spaces that break regex
    return t

#######################################################################################################################
# Function that prepares a cropped image of a card's attack and defense for tesseract
# Parameters: the original cropped image
# Returns: the preprocessed version of the image
#######################################################################################################################
def preprocess_atkdef(img):
    gray = img.convert("L") # converts the image to greyscale using Pillow's 'L' mode
    gray = ImageOps.autocontrast(gray) # removes color information, leaving only brightness levels for OCR
    gray = gray.resize((gray.width * 3, gray.height * 3), Image.LANCZOS) # increase the size of the image

    # make edges of image cripser with a sharp mask
    # radius=1 is how far around each pixel to look
    # percent = how strong the sharpening effect is
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=150))
    return gray

#######################################################################################################################
# Function saves each image produced by cropping the original card image by saving the images for viewing/debugging
# Parameters: the regions used for cropping
# Returns: void
#######################################################################################################################
def debug_show_crops(regions):
    # loop through every key in the regions dictionary and the img associated with that region
    for key, img in regions.items():
        # make a safe filename by replacing anything not a letter, number, underscore or hyphen with an underscore
        safe_key = re.sub(r'[^a-zA-Z0-9_-]', '_', key)
        img.save(f"processed_pics/{safe_key}.png") # save the image for viewing what the cropped image looks like
        # img.show(title=key) # only uncomment if you wish to display all cropped images

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

#######################################################################################################################
# Function that performs ocr on an image and return the text extracted as a dictionary
# Parameters: the image to be scanned and optional configurations if desired
# Returns: the image's text information as a dictionary for more structured analysis (like skipping unsure words)
#######################################################################################################################
def ocr_data(img, config=""):
    """Return tesseract data as a dictionary to inspect word confidences."""
    # Use the default engine mode for tesseract since it's more accurate
    # append any optional configurations
    cfg = ("--oem 3 " + config).strip()

    # perform ocr to get each word detected, output as a dictionary instead of plain text, pass in configurations
    return pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=cfg)

#######################################################################################################################
# Function that takes data returned by ocr and only keeps words that pass a certain confidence level
# Parameters: the ocr data and the minimum confidence level for a word
# Returns: only a list of words that pass the confidence test
#######################################################################################################################
def ocr_text_from_data(data, min_conf=60):
    """Assembles the words detected by ocr while only keeping words with high confidence level"""
    words = [] # for storing words that pass confidence test

    # iterate through each word detected by tesseract and sanitize it for analysis
    for index, word in enumerate(data.get('text', [])):
        txt = word.strip()

        # if the resulting word is empty, continue to the next word
        if not txt:
            continue

        # attempt to extract the confidence level for the word by its corresponding index
        # sometimes tesseract returns level as a string, so wrap in try/except just in case and return -1 if fails
        try:
            conf = int(float(data['conf'][index]))
        except:
            conf = -1

        # only keep the word if it's above the minimum confidence level
        if conf >= min_conf:
            words.append(txt)

    # join the list together with a space separator
    return " ".join(words).strip()

#######################################################################################################################
# Function that cleans up and fixes common character misreads by ocr for a card's name
# Parameters: the raw string for the card's name
# Returns: a cleaned and standard format for the name as a string
#######################################################################################################################
def correct_chars_for_name(raw):
    cleaned_string = raw.upper()  # first, uppercase everything

    # define a dictionary representing common character misreads by ocr and their proper replacement characters
    CHAR_FIXES = {'0': 'O','1': 'I','5': 'S','6': 'G','8': 'B','|': 'I','¢': 'C'}

    # iterate through each character in the original string
    # if character exists in CHAR_PIXES, replace it with the dictionary value. otherwise keep it unchanged
    cleaned_string = "".join(CHAR_FIXES.get(ch, ch) for ch in cleaned_string)

    cleaned_string = re.sub(r"[^A-Z0-9\s\-]", "", cleaned_string) # allow letters, numbers, spaces, hyphens
    cleaned_string = re.sub(r"\s{2,}", " ", cleaned_string).strip() # collapse multiple spaces
    cleaned_string = " ".join(w.capitalize() for w in cleaned_string.split()) # capitalize each word
    return cleaned_string

#######################################################################################################################
# Function that crops a Yugioh card image into 5 regions containing the information we need
# Parameters: the original card image
# Returns: a dictionary of the cropped image sections
#######################################################################################################################
def crop_regions(img):
    """Crops the 5 major text zones of a YuGiOh card."""
    w, h = img.size # retrieve the width and height of the image

    # define the coordinates for Pillow's crop() function (left, upper, right, lower)
    # ex for name_box: starting bit = 7% from left, next bit = 5% from top, last = 80% from right and 13% from bottom
    name_box = (int(0.07*w), int(0.05*h), int(0.80*w), int(0.13*h))
    attribute_box = (int(0.80*w), int(0.07*h), int(0.91*w), int(0.15*h))
    type_box = (int(0.08 * w),int(0.73 * h),(0.70 * w),int(0.78 * h))
    desc_box = (int(0.07*w), int(0.68*h), int(0.93*w), int(0.87*h))
    atk_def_box = (int(0.50*w), int(0.89*h), int(0.89*w), int(0.93*h))
    return {
        "name": img.crop(name_box),
        "attribute": img.crop(attribute_box),
        "type": img.crop(type_box),
        "description": img.crop(desc_box),
        "atkdef": img.crop(atk_def_box)
    }

#######################################################################################################################
# Function that prepares an image of a card's name for OCR
# Parameters: the original cropped image
# Returns: the preprocessed version of the image
#######################################################################################################################
def preprocess_name(img):
    """Used to prepare a cropped card name image for ocr"""
    gray = img.convert("L") # convert image to grayscale
    gray = ImageOps.autocontrast(gray) # increase the contrast for better recondition
    # remove noise by replacing each pixel with the median of its neighbor
    gray = gray.filter(ImageFilter.MedianFilter(3))
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=150)) # sharpen the edges of card text etc.
    return gray.resize((gray.width * 3, gray.height * 3), Image.LANCZOS) # enlarge image with LANCZOS filter

#######################################################################################################################
# Function used to prepare a card's cropped attribute icon and a known icon for equal match comparison
# Parameters: the original cropped image of the card's attribute icon and a known one in the "attributes" folder
# Returns: a processed version of the image supplied
#######################################################################################################################
def preprocess_attr_for_match(img):
    gray = img.convert("L") # convert to grayscale
    gray = gray.resize((64 * 4, 64 * 4), Image.LANCZOS) # resize images to predefined size
    gray = gray.filter(ImageFilter.MedianFilter(3)) # remove noise by replacing each pixel with the median of neighbor
    gray = ImageEnhance.Contrast(gray).enhance(1.4) # increase contrast to make elements stand out
    gray = ImageEnhance.Brightness(gray).enhance(0.9) # increase brightness
    gray = gray.filter(ImageFilter.EDGE_ENHANCE_MORE) # sharpens the edges of elements like text
    gray = ImageOps.autocontrast(gray) # perform auto-contrast to stretch image and remove washed out values in graph
    return gray

#######################################################################################################################
# Function used to prepare a card's cropped attribute icon for OCR
# Parameters: the original cropped image of the card's attribute icon
# Returns: a processed version of the image supplied
#######################################################################################################################
def preprocess_attribute(img):
    """
    Prepares the cropped image of a card's attribute icon for OCR
    """
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS) # increase image size
    img = img.filter(ImageFilter.MedianFilter(size=3))# remove noise by replacing each pixel with the median of neighbor
    img = ImageOps.autocontrast(img, cutoff=4) # Increase all pixel's contrast except the more extreme black/whites

    return img

#######################################################################################################################
# Function used to prepare and image of a card's card_type for OCR
# Parameters: the original cropped image
# Returns: a processed version of the image supplied
#######################################################################################################################
def preprocess_type(img):
    """Used to prepare a cropped card_type image for ocr"""
    gray = img.convert("L") # convert to grayscale
    gray = ImageOps.autocontrast(gray) # perform auto-contrast enhancement
    gray = gray.resize((gray.width * 6, gray.height * 6), Image.LANCZOS) # enlarge
    gray = gray.filter(ImageFilter.MedianFilter(3)) # remove noise
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=250)) # sharpen edges of text etc.
    gray = ImageEnhance.Contrast(gray).enhance(1.5) # increase contrast some more
    return gray

#######################################################################################################################
# Function used to prepare and image of a card's card_type for OCR
# Parameters: the original cropped image
# Returns: a processed version of the image supplied
#######################################################################################################################
def preprocess_desc(img):
    """Used to prepare a cropped card description image for ocr"""
    gray = img.convert("L")
    gray = gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)
    gray = gray.filter(ImageFilter.MedianFilter(3))
    return gray

#######################################################################################################################
# Function used to analyze the extracted text for a card's monster_type for it's best match in KNOWN_TYPES
# Parameters: raw monster_type text extracted by ORC
# Returns: the best match for monster_type and the extracted text
#######################################################################################################################
def match_monster_type(type_raw):
    # return a cleaned up version. If nothing is return by this process, return an empty string
    cleaned = clean_raw_type(type_raw)
    if not cleaned:
        return ""

    # convert cleaned text into a set of characters for inspection
    cleaned_set = set(cleaned)

    # if the cleaned text are common misreads for "Dragon", return "DRAGON"
    if cleaned in ("TD", "FD", "RD", "ID", "DD", "D"):
        return "DRAGON"

    # initialize variables for storing the best monster_type match as a string and the best similarity score
    best = None
    best_score = -999

    #
    for t in KNOWN_TYPES:
        # remove any dashes or empty spaces from KNOWN_TYPE and convert result to a set of characters
        t_clean = t.replace("-", "").replace(" ", "")
        t_set = set(t_clean)

        # Calculate the similarity score by dividing the number of characters shared by the known type's length
        score = len(cleaned_set & t_set) / len(t_clean)

        # if the current iteration's score is higher, it's a better match.
        # Replace that with best_score, as assign the corresponding known type to be returned
        if score > best_score:
            best_score = score
            best = t

    # if match is extremely weak, return raw OCR
    if best_score < 0.2:
        return cleaned

    return best

#######################################################################################################################
# Function used to process an entire card image and extract its individual data
# Parameters: the filepath to the image to analyze
# Returns: a dictionary representing the card's information
#######################################################################################################################
def process_yugioh_card(image_path):
    # open the image, crop into each region of the card that has the data we need, and save each crop for debugging
    original = Image.open(image_path)
    regions = crop_regions(original)
    debug_show_crops(regions)

    # ---------- Preprocess each cropped region ----------
    name_img = preprocess_name(regions["name"])
    attribute_img = preprocess_attribute(regions["attribute"])
    type_img = preprocess_type(regions["type"])
    desc_img = preprocess_desc(regions["description"])
    atkdef_img = preprocess_atkdef(regions["atkdef"])

    # ---------- Extract name data ----------
    name_data = ocr_data(name_img, config="--psm 7") # perform ocr. --psm7 treats are a single line of text
    raw_name = ocr_text_from_data(name_data, min_conf=50) # parse ocr data into raw text
    name_clean = correct_chars_for_name(raw_name) # clean up the raw text

    # ---------- Attribute ----------
    attribute = classify_attribute(attribute_img) # match the attribute image to its best match in "attribute" folder

    # ---------- Monster Type ----------
    # perform ocr and only recognize the supplied list of characters
    type_data = ocr_data(type_img, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ[]")
    type_raw = ocr_text_from_data(type_data, min_conf=45) # keep only words with a certain confidence level
    type_clean = match_monster_type(type_raw) # find the raw text's best match in KNOWN_TYPES

    # ---------- DESCRIPTION ----------
    desc_data = ocr_data(desc_img, config="--psm 6") # perform ocr as a block of text using page segmentation mode 6
    description_raw = ocr_text_from_data(desc_data, min_conf=45) # keeps only data that meets confidence requirements
    description = re.sub(r'\b[A-Z]{1,2}\b', '', description_raw) # only keep non-isolated A-Z.
    description = re.sub(r'[\|\=\>\<\&]', '', description) # remove symbols
    description = re.sub(r'\s{2,}', ' ', description).strip() # normalize spacing

    # ---------- ATK/DEF ----------
    atkdef_raw = pytesseract.image_to_string(atkdef_img, config="--psm 7").strip() # extract raw ATK/DEF data

    # ----------IMAGE FILEPATH -----
    filename = os.path.basename(image_path) # only keep non-nested base name

    # Fix common misreads in labels only with a function to replace the labels with a corrected version
    def fix_atkdef_labels(text):
        t = text.upper()
        t = t.replace("ALK", "ATK")
        t = t.replace("DFF", "DEF")
        t = t.replace("DE8", "DEF")
        t = t.replace("DEF/", "DEF:")
        t = t.replace("ATK/", "ATK:")
        return t

    # apply label fixes as needed
    atkdef_fixed_labels = fix_atkdef_labels(atkdef_raw)

    # Extract numbers using a pattern-matching function
    def extract_atk_def_numbers(text):
        # define pattern to use for matching
        patterns = [
            r'ATK[:]?(\d{2,5})\D+DEF[:]?(\d{2,5})',  # allow non-digits between numbers
            r'(\d{2,5})/(\d{2,5})',
            r'(\d{2,5})\s+(\d{2,5})'
        ]
        # loop through every pattern and attempt to match with the given text
        for pat in patterns:
            match = re.search(pat, text)
            # if a match is found, normalize the data and return it. Otherwise return nothing for ATK and DEF
            if match:
                # Normalize digits inside numbers only
                #{'O':'0', 'D':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8'}
                DIGIT_FIX = {'O':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8'}
                atk = int("".join(DIGIT_FIX.get(ch, ch) for ch in match.group(1)))
                defe = int("".join(DIGIT_FIX.get(ch, ch) for ch in match.group(2)))
                return atk, defe
        return None, None
    atk, defn = extract_atk_def_numbers(atkdef_fixed_labels)

    # ---------- CARD TYPE ----------
    # if the card has an attack value, it's type is a monster. otherwise match its type with its attribute
    if atk is not None:
        card_type = "Monster"
    elif attribute == "SPELL":
        card_type = "Spell"
    elif attribute == "TRAP":
        card_type = "Trap"
    else:
        card_type = "Unknown"

    # return final result as a dictionary
    return {
        "name": name_clean,
        "attribute": attribute,
        "monster_type": type_clean,
        "description": description,
        "attack": atk,
        "defense": defn,
        "card_type": card_type,
        "image_filename": filename
    }
