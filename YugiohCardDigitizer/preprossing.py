###################################################################################################
# Yu-Gi-Oh Card OCR System
# Extracts: name, attribute, type, description, ATK, DEF
# Works on clean, unprocessed card images photographed/scanned
###################################################################################################
import difflib
import os

# imports
from PIL import Image, ImageOps, ImageFilter, ImageEnhance  # for image manipulation
import pytesseract                              # for ocular recognition functionality
import re                                       # for pattern matching text extracted from cards
import numpy as np

DIGIT_FIX = {'O':'0', 'D':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8'} # for mapping common OCR misreads to correct digits
# define a list of all monster types for matching
KNOWN_TYPES = [
    "AQUA", "BEAST", "BEAST-WARRIOR", "CREATOR GOD", "CYBERSE", "DINOSAUR",
    "DIVINE-BEAST", "DRAGON", "FAIRY", "FIEND", "FISH", "INSECT", "MACHINE",
    "PLANT", "PSYCHIC", "PYRO", "REPTILE", "ROCK", "SEA SERPENT",
    "SPELLCASTER", "THUNDER", "WARRIOR", "WINGED BEAST", "WYRM", "ZOMBIE"
]
# Common OCR corrections for Yu-Gi-Oh monster types
COMMON_FIXES = {
    "0": "O",
    "1": "I",
    "5": "S",
    "6": "G",
    "8": "B",
    "4": "A",
    "|": "I",
    "{": "[",
    "}": "]",
}

def clean_raw_type(text):
    """Normalize raw OCR output before matching."""
    if not text:
        return ""

    t = text.upper().strip()

    # Apply common OCR corrections
    t = "".join(COMMON_FIXES.get(c, c) for c in t)

    # Remove anything not A–Z, space, bracket, or dash
    t = re.sub(r"[^A-Z\[\]\- ]", "", t)

    # Strip brackets for matching
    t = t.replace("[", "").replace("]", "").strip()

    return t


def safe_fuzzy_match(raw):
    """Safely match against known types without overcorrecting."""

    # If OCR returned something extremely short (e.g., "TD"), do NOT guess.
    if len(raw) < 4:
        return raw  # too short to safely autocorrect

    # Try direct fuzzy match
    match = difflib.get_close_matches(raw, KNOWN_TYPES, n=1, cutoff=0.6)

    if match:
        return match[0]

    # As a fallback, allow slightly looser matching ONLY if very close
    loose = difflib.get_close_matches(raw, KNOWN_TYPES, n=1, cutoff=0.45)
    if loose:
        # Prevent catastrophic mismatches: ensure similarity ratio > 0.6
        if difflib.SequenceMatcher(None, raw, loose[0]).ratio() > 0.60:
            return loose[0]

    return raw  # if everything fails, keep as-is

def guess_monster_type(text):
    inside = text.strip("[]").strip()

    # 1. Try fuzzy match with a lower cutoff
    match = difflib.get_close_matches(inside, KNOWN_TYPES, n=1, cutoff=0.2)
    if match:
        return f"{match[0]}"

    # 2. Levenshtein-distance fallback (manual)
    def edit_dist(a,b):
        dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
        for i in range(len(a)+1):
            dp[i][0] = i
        for j in range(len(b)+1):
            dp[0][j] = j
        for i in range(1, len(a)+1):
            for j in range(1, len(b)+1):
                cost = 0 if a[i-1] == b[j-1] else 1
                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + cost
                )
        return dp[-1][-1]

    best = None
    best_score = 999

    for t in KNOWN_TYPES:
        d = edit_dist(inside, t)
        if d < best_score:
            best_score = d
            best = t

    # 3. Require normalized distance < 0.6 to accept
    if best and best_score / len(best) <= 0.6:
        return f"{best}"

    return text
def normalize_type_text(t):
    t = t.upper().strip()

    # common OCR errors
    t = t.replace("0", "O")
    t = t.replace("1", "I")
    t = t.replace("8", "B")
    t = t.replace("{", "[")
    t = t.replace("}", "]")
    t = t.replace("]", "]")  # ensure at least one
    t = t.replace("[ ", "[")
    t = t.replace(" ]", "]")

    # remove stray characters tesseract often produces
    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ[]- "
    t = "".join(c for c in t if c in allowed)

    # force bracket format if missing
    if not t.startswith("["):
        t = "[" + t
    if not t.endswith("]"):
        t += "]"

    return t


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
    CHAR_FIXES = {
        '0': 'O',
        '1': 'I',
        '5': 'S',
        '6': 'G',
        '8': 'B',
        '|': 'I',
        '¢': 'C'
    }

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
    img.crop(type_box).save("DEBUG_type_crop.png")
    return {
        "name": img.crop(name_box),
        "attribute": img.crop(attribute_box),
        "type": img.crop(type_box),
        "description": img.crop(desc_box),
        "atkdef": img.crop(atk_def_box)
    }

def preprocess_name(img):
    """Used to prepare a cropped card name image for ocr"""
    gray = img.convert("L")
    gray = ImageOps.autocontrast(gray)
    gray = gray.filter(ImageFilter.MedianFilter(3))
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=150))
    return gray.resize((gray.width * 3, gray.height * 3), Image.LANCZOS)

def preprocess_attr_for_match(img):
    g = img.convert("L")
    g = g.resize((64 * 4, 64 * 4), Image.LANCZOS)
    g = g.filter(ImageFilter.MedianFilter(3))
    g = ImageEnhance.Contrast(g).enhance(1.4)
    g = ImageEnhance.Brightness(g).enhance(0.9)
    g = g.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # NEW: normalize brightness/contrast to improve matching
    g = ImageOps.autocontrast(g)
    g.resize((64, 64), Image.LANCZOS)
    return g

def preprocess_attribute(img):
    """
    Very light preprocessing for attribute icons — keep color & structure!
    """
    # Slight upscale for stability
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

    # Gentle denoise (small median filter)
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Mild autocontrast but NOT full dynamic range
    img = ImageOps.autocontrast(img, cutoff=4)

    return img



def preprocess_type(img):
    """Used to prepare a cropped card_type image for ocr"""
    gray = img.convert("L")
    gray = ImageOps.autocontrast(gray)
    gray = gray.resize((gray.width * 6, gray.height * 6), Image.LANCZOS)  # bigger upscale
    gray = gray.filter(ImageFilter.MedianFilter(3))
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=250))       # stronger
    gray = ImageEnhance.Contrast(gray).enhance(1.5)
    gray.save("processed_pics/processed_monsterType.png")
    return gray


def preprocess_desc(img):
    """Used to prepare a cropped card description image for ocr"""
    gray = img.convert("L")
    gray = gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)
    gray = gray.filter(ImageFilter.MedianFilter(3))
    return gray

def extract_monster_type(type_raw):
    cleaned = clean_raw_type(type_raw)
    if not cleaned:
        return ""

    cleaned_set = set(cleaned)

    # --- SPECIAL CASES -----------------------------------------------------
    # If OCR gives "TD", "FD", "RD", "ID", etc → usually DRAGON
    # Dragon's [D] is the darkest, boldest letter in the type box.
    if cleaned in ("TD", "FD", "RD", "ID", "DD", "D"):
        return "DRAGON"

    # If the cleaned string starts with D and is short → also Dragon
    if cleaned.startswith("D") and len(cleaned) <= 3:
        return "DRAGON"

    # --- GENERAL LETTER-OVERLAP LOGIC --------------------------------------
    best = None
    best_score = -999

    for t in KNOWN_TYPES:
        t_clean = t.replace("-", "").replace(" ", "")
        t_set = set(t_clean)

        score = len(cleaned_set & t_set) / len(t_clean)

        if score > best_score:
            best_score = score
            best = t

    # if match is extremely weak, return raw OCR
    if best_score < 0.2:
        return cleaned

    return best

def process_yugioh_card(image_path):
    original = Image.open(image_path)
    regions = crop_regions(original)
    debug_show_crops(regions)

    # ---------- Preprocessing ----------
    name_img      = preprocess_name(regions["name"])
    attribute_img = preprocess_attribute(regions["attribute"])
    type_img      = preprocess_type(regions["type"])
    desc_img      = preprocess_desc(regions["description"])
    atkdef_img    = preprocess_atkdef(regions["atkdef"])

    # ---------- NAME ----------
    name_data = ocr_data(name_img, config="--psm 7")
    raw_name = ocr_text_from_data(name_data, min_conf=50)
    name_clean = correct_chars_for_name(raw_name)

    # ---------- ATTRIBUTE ----------
    attribute = classify_attribute(attribute_img)

    # ---------- TYPE ----------
    type_data = ocr_data(type_img, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ[]")
    type_raw = ocr_text_from_data(type_data, min_conf=45)
    type_clean = extract_monster_type(type_raw)
    print(f"type data: {type_data}")
    print(f"type data raw: {type_raw}")
    print(f"type data clean: {type_clean}")

    # ---------- DESCRIPTION ----------
    desc_data = ocr_data(desc_img, config="--psm 6")
    description_raw = ocr_text_from_data(desc_data, min_conf=45)
    description = re.sub(r'\b[A-Z]{1,2}\b', '', description_raw)
    description = re.sub(r'[\|\=\>\<\&]', '', description)
    description = re.sub(r'\s{2,}', ' ', description).strip()

    # ---------- ATK/DEF ----------
    atkdef_raw = pytesseract.image_to_string(atkdef_img, config="--psm 7").strip()

    # ----------IMAGE FILEPATH -----
    filename = os.path.basename(image_path)

    # Fix common misreads in labels only
    def fix_atkdef_labels(text):
        t = text.upper()
        t = t.replace("ALK", "ATK")
        t = t.replace("DFF", "DEF")
        t = t.replace("DE8", "DEF")
        t = t.replace("DEF/", "DEF:")
        t = t.replace("ATK/", "ATK:")
        return t

    atkdef_fixed_labels = fix_atkdef_labels(atkdef_raw)

    # Extract numbers
    def extract_atk_def_numbers(text):
        # Look for numbers with optional ATK/DEF prefixes
        patterns = [
            r'ATK[:]?(\d{2,5})\D+DEF[:]?(\d{2,5})',  # allow non-digits between numbers
            r'(\d{2,5})/(\d{2,5})',
            r'(\d{2,5})\s+(\d{2,5})'
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                # Normalize digits inside numbers only
                DIGIT_FIX = { 'O':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8' }
                atk = int("".join(DIGIT_FIX.get(ch, ch) for ch in m.group(1)))
                defe = int("".join(DIGIT_FIX.get(ch, ch) for ch in m.group(2)))
                return atk, defe
        return None, None

    atk, defn = extract_atk_def_numbers(atkdef_fixed_labels)

    # ---------- CARD TYPE INFERENCE ----------
    if atk is not None:
        card_type = "Monster"
    elif attribute == "SPELL":
        card_type = "Spell"
    elif attribute == "TRAP":
        card_type = "Trap"
    else:
        card_type = "Unknown"

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


