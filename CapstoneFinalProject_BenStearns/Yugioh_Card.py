class YugiohCard:
    # constructor for instantiating a Yugioh card object
    def __init__(self, name, description, attack, defense, type, color):
        self.name = name
        self.description = description
        self.attack = attack
        self.defense = defense
        self.type = type
        self.color = color

def __repr__(self):
    return (f"YugiohCard(name='{self.name}', type='{self.type}', "
            f"ATK={self.attack}, DEF={self.defense}, color='{self.color}')")