class YugiohCard:
    # constructor for instantiating a Yugioh card object
    def __init__(self,name,card_type,description,monster_type=None,attribute=None,
                 attack=None,defense=None,image_filename=None):
        self.name = name
        self.description = description
        self.attack = attack
        self.defense = defense
        self.card_type = card_type
        self.attribute = attribute
        self.monster_type = monster_type
        self.image_filename = image_filename

def __repr__(self):
    return (f"YugiohCard(name='{self.name}', card_type='{self.card_type}', description='{self.description}', "
            f"attribute='{self.attribute}, monster_type='{self.monster_type}', "
            f"ATK={self.attack}, DEF={self.defense}', image_filename='{self.image_filename}')")