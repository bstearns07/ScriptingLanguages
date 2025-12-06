###################################################################################################
# Yu-Gi-Oh Card OCR System
# Extracts: name, attribute, type, description, ATK, DEF
# Works on clean, unprocessed card images photographed/scanned
###################################################################################################
import os

# imports
from PIL import Image, ImageOps, ImageFilter, ImageEnhance  # for image manipulation
import pytesseract                              # for ocular recognition functionality
import re                                       # for pattern matching text extracted from cards

DIGIT_FIX = {'O':'0', 'D':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8'} # for mapping common OCR misreads to correct digits

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
        # img.show(title=key)

def classify_attribute(cropped_attr_img, template_dir="attributes"):
    """
    Histogram-matching classifier with equal preprocessing.
    """
    # Preprocess the cropped icon exactly like the templates
    img = preprocess_attr_for_match(cropped_attr_img)
    img_hist = img.histogram()

    best_match = None
    best_score = float("inf")

    for filename in os.listdir(template_dir):
        if not filename.lower().endswith(".png"):
            continue

        label = filename.split(".")[0].upper()

        template = Image.open(os.path.join(template_dir, filename))

        # Apply the same processing to templates
        template = preprocess_attr_for_match(template)
        template_hist = template.histogram()

        score = sum((a - b) ** 2 for a, b in zip(img_hist, template_hist))

        if score < best_score:
            best_score = score
            best_match = label

    return best_match

def ocr_data(img, config=""):
    """Return tesseract 'data' dictionary so we can inspect word confidences."""
    # Use OEM 3 (LSTM) by default unless you have a reason not to
    cfg = ("--oem 3 " + config).strip()
    return pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=cfg)

def ocr_text_from_data(data, min_conf=60):
    """Assemble text from image_to_data output, skipping low-confidence words."""
    words = []
    for i, w in enumerate(data.get('text', [])):
        txt = w.strip()
        if not txt:
            continue
        try:
            conf = int(float(data['conf'][i]))
        except:
            conf = -1
        if conf >= min_conf:
            words.append(txt)
    # join with space; caller will clean up punctuation as needed
    return " ".join(words).strip()

# Basic char-correction to fix common OCR mistakes
CHAR_FIXES = {
    '0': 'O',  # zero -> letter O if in name
    '1': 'I',
    '5': 'S',
    '6': 'G',
    '8': 'B',
    '|': 'I',
    '¢': 'c'
}

def correct_chars_for_name(raw):
    s = raw.upper()  # first, uppercase everything
    # apply likely OCR misreads corrections
    CHAR_FIXES = {
        '0': 'O',
        '1': 'I',
        '5': 'S',
        '6': 'G',
        '8': 'B',
        '|': 'I',
        '¢': 'C'
    }
    s = "".join(CHAR_FIXES.get(ch, ch) for ch in s)
    # allow letters, numbers, spaces, hyphens
    s = re.sub(r"[^A-Z0-9\s\-]", "", s)
    # collapse multiple spaces
    s = re.sub(r"\s{2,}", " ", s).strip()
    # optional: capitalize each word
    s = " ".join(w.capitalize() for w in s.split())
    return s


def normalize_atkdef_text(text):
    """Convert OCR-misread characters to digits and uppercase text."""
    return "".join(DIGIT_FIX.get(ch, ch) for ch in text.upper())

def extract_atk_def_from_text(text):
    if not text:
        return None, None

    # Normalize OCR digits
    DIGIT_FIX = { 'O':'0', 'D':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8' }
    text_norm = "".join(DIGIT_FIX.get(ch, ch) for ch in text.upper())

    # Fix misread labels
    text_norm = fix_atkdef_labels(text_norm)

    # Regex patterns
    patterns = [
        r'ATK[:]?([0-9]{2,5})DEF[:]?([0-9]{2,5})',  # ATK:3000DEF:2500
        r'([0-9]{2,5})/([0-9]{2,5})',               # 3000/2500
        r'([0-9]{2,5})([0-9]{2,5})'                 # fallback
    ]

    for pat in patterns:
        m = re.search(pat, text_norm)
        if m:
            try:
                return int(m.group(1)), int(m.group(2))
            except:
                continue
    return None, None

def crop_regions(img):
    """Crop the 5 major text zones of a Yu-Gi-Oh card."""
    w, h = img.size

    # Adjust these as needed based on your input images.
    name_box       = (int(0.07*w), int(0.05*h), int(0.80*w), int(0.13*h))
    attribute_box  = (int(0.80*w), int(0.07*h), int(0.91*w), int(0.15*h))
    type_box       = (int(0.07*w), int(0.60*h), int(0.93*w), int(0.68*h))
    desc_box       = (int(0.07*w), int(0.68*h), int(0.93*w), int(0.87*h))
    atkdef_box     = (int(0.50*w), int(0.89*h), int(0.89*w), int(0.93*h))

    return {
        "name": img.crop(name_box),
        "attribute": img.crop(attribute_box),
        "type": img.crop(type_box),
        "description": img.crop(desc_box),
        "atkdef": img.crop(atkdef_box)
    }

def preprocess_name(img):
    """Enhance name region for OCR accuracy."""
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

    return g.resize((64, 64), Image.LANCZOS)


def preprocess_attribute(img):
    """
    Best preprocessing for low-res Yu-Gi-Oh attribute icons using ONLY Pillow.
    - Early upscaling
    - Mild noise cleaning
    - Local contrast boost
    - Gentle edge enhancement
    """
    # 1. Convert to grayscale
    gray = img.convert("L")

    # 2. Upscale early (super important)
    gray = gray.resize((gray.width * 4, gray.height * 4), Image.LANCZOS)

    # 3. Mild denoise: small median filter
    gray = gray.filter(ImageFilter.MedianFilter(size=3))

    # 4. Local contrast boost (Pillow's closest to CLAHE)
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.4)      # Light contrast boost

    # 5. Light brightness adjustment to deepen text
    enhancer = ImageEnhance.Brightness(gray)
    gray = enhancer.enhance(0.9)

    # 6. Gentle edge enhance (safer than UnsharpMask)
    gray = gray.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # 7. Do NOT threshold — keep grayscale to avoid destroying detail
    #gray.show()
    gray.save("processed_pics/processed_attribute.png")
    return gray


def preprocess_type(img):
    gray = img.convert("L")
    gray = ImageOps.autocontrast(gray)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=80))
    return gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)


def preprocess_desc(img):
    gray = img.convert("L")
    gray = gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)
    gray = gray.filter(ImageFilter.MedianFilter(3))
    return gray

def ocr(img, config=""):
    """Run Tesseract OCR with given config."""
    return pytesseract.image_to_string(img, config=config).strip()


def extract_atk_def(text):
    atk = defn = None
    match = re.search(r"ATK\s*[:/ ]\s*(\d+)\D+DEF\s*[:/ ]\s*(\d+)", text)
    if match:
        atk = int(match.group(1))
        defn = int(match.group(2))
    return atk, defn


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
    attribute_img.show()

    # ---------- TYPE ----------
    type_data = ocr_data(type_img, config="--psm 7")
    type_raw = ocr_text_from_data(type_data, min_conf=45)
    type_clean = re.sub(r'[^A-Z\[\]\s\-]', '', type_raw.upper())

    # ---------- DESCRIPTION ----------
    desc_data = ocr_data(desc_img, config="--psm 6")
    description_raw = ocr_text_from_data(desc_data, min_conf=45)
    description = re.sub(r'\b[A-Z]{1,2}\b', '', description_raw)
    description = re.sub(r'[\|\=\>\<\&]', '', description)
    description = re.sub(r'\s{2,}', ' ', description).strip()

    # ---------- ATK/DEF ----------
    atkdef_raw = pytesseract.image_to_string(atkdef_img, config="--psm 7").strip()

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

    return {
            "name": name_clean,
            "attribute": attribute,
            "type": type_clean,
            "description": description,
            "atk": atk,
            "def": defn
        }

