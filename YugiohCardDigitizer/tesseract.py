########################################################################################################################
# Title..............: Capstone Final Project - Ocular Recognition
# Author.............: Ben Stearns
# Date...............: 10-30-2025
# Purpose............: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: defines a function to run the tesseract program on all image files
#######################################################################################################################
# REQUIRED: Download tesseract here => https://github.com/UB-Mannheim/tesseract/wiki
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# python.org/downloads/release/python-3127
# imports
import os

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import sqlite3
import DBcm
from preprossing import preprocess_image    # for use of the preprocess_image() function
from extractor import extract_text          # for use of the extract_text() function
from utils import extract_card_info      # for use of the extract_contact_info() function
from Yugioh_Card import YugiohCard

images_dir = "samples"
db_details ="Cards.sqlite3"

def main():
    for file in os.listdir(images_dir):
        image_filepath = os.path.join(images_dir, file)
        processed_image = preprocess_image(image_filepath)
        text = extract_text(processed_image)
        card = extract_card_info(text)

        processed_image.save("tesseractImage.png")

        print("===Extracted Text===")
        print(text)
        print("===Image Information===")
        print(card.name, card.attack, card.defense, card.type, card.color)
        print(card.description)
        print()

        with DBcm.UseDatabase(db_details) as db:
            SQL = """create table if not exists cards (
                    id integer not null primary key autoincrement,
                    name varchar(32) not null,
                    attack integer,
                    defense integer,
                    description varchar(500) not null,
                    type varchar(32),
                    color varchar(32) not null      
                )"""
            db.execute(SQL)
            blue_eyes = YugiohCard(
                name="Blue-Eyes White Dragon",
                description="This legendary dragon is a powerful engine of destruction.",
                attack=3000,
                defense=2500,
                type="Dragon",
                color="Light"
            )
            dark_magician = YugiohCard(
                name="Dark Magician",
                description = "The ultimate wizard in terms of attack and defense.",
                attack=2500,
                defense=2000,
                type="Spellcaster",
                color="Yellow"
            )
            insert_SQL = """
                INSERT INTO cards (name, attack, defense, description, type, color)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            db.execute(insert_SQL, (
                dark_magician.name,
                dark_magician.attack,
                dark_magician.defense,
                dark_magician.description,
                dark_magician.type,
                dark_magician.color
            ))
            db.execute("SELECT * FROM cards")
            print(f"Cards in table: {db.fetchall()}")
            db.execute("pragma table_list")
            results = db.fetchall() #returns most recent command executed
            print(f"Results: {results}")

if __name__ == "__main__":
    main()
