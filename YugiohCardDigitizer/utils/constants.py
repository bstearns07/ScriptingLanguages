
# define a list of all monster types for matching
KNOWN_TYPES = [
    "AQUA", "BEAST", "BEAST-WARRIOR", "CREATOR GOD", "CYBERSE", "DINOSAUR",
    "DIVINE-BEAST", "DRAGON", "FAIRY", "FIEND", "FISH", "INSECT", "MACHINE",
    "PLANT", "PSYCHIC", "PYRO", "REPTILE", "ROCK", "SEA SERPENT",
    "SPELLCASTER", "THUNDER", "WARRIOR", "WINGED BEAST", "WYRM", "ZOMBIE"
]

# Common OCR corrections for Yu-Gi-Oh monster types
COMMON_FIXES = {"0": "O","1": "I","5": "S","6": "G","8": "B","4": "A","|": "I","{": "[","}": "]",}
