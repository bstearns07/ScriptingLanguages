import re


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
    t = t.replace("DEF:", " DEF:")  # ensures a separator
    return t

# # Fix common misreads in labels only with a function to replace the labels with a corrected version
# def fix_atkdef_labels(text):
#     t = text.upper()
#     t = t.replace("ALK", "ATK")
#     t = t.replace("DFF", "DEF")
#     t = t.replace("DE8", "DEF")
#     t = t.replace("DEF/", "DEF:")
#     t = t.replace("ATK/", "ATK:")
#     return t

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
        # if a match is found, normalize the data and return it. Otherwise, return nothing for ATK and DEF
        if match:
            # Normalize digits inside numbers only
            #{'O':'0', 'D':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8'}
            DIGIT_FIX = {'O':'0', 'I':'1', 'L':'1', 'S':'5', 'B':'8'}
            atk = int("".join(DIGIT_FIX.get(ch, ch) for ch in match.group(1)))
            defe = int("".join(DIGIT_FIX.get(ch, ch) for ch in match.group(2)))
            return atk, defe
    return None, None