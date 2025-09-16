import random

suits = ["Clubs","Spades","Hearts","Diamonds"]
faces = ["Jack","Queen","King","Ace"]
numbered = [2,3,4,5,6,7,8,9,10]

deck = set()
for suit in suits:
    for card in faces + numbered:
        deck.add((card, "of", suit))

print(f"There are {len(deck)} cards in the deck")

def Draw():
    card = random.choice(list(deck))
    deck.remove(card)
    return f"You drew the {card}"

print(Draw())
print(f"Now you have {len(deck)} cards in the deck")

cardToCheck = ("King", "of", "Hearts")

if cardToCheck in deck:
    print(f"{cardToCheck} was successfully found in the deck")
else:
    print(f"{cardToCheck} was NOT found in the deck")