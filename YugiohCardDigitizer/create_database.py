from Yugioh_Card import YugiohCard
import sqlite3
import DBcm

db_details ="Cards.sqlite3"
insert_SQL = """
    INSERT INTO cards (name, card_type, monster_type, description, attack, defense, attribute)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

with DBcm.UseDatabase(db_details) as db:
    SQL = """create table if not exists cards (
            id integer not null primary key autoincrement,
            name varchar(32) not null,
            card_type varchar(32) not null,
            monster_type varchar(32),  
            description varchar(500) not null,  
            attack integer,
            defense integer,
            attribute varchar(32) not null
        )"""
    db.execute(SQL)
    blue_eyes = YugiohCard(
        name="Blue-Eyes White Dragon",
        card_type="Monster",
        monster_type="Dragon",
        description="This legendary dragon is a powerful engine of destruction.",
        attack=3000,
        defense=2500,
        attribute="Light"
    )
    dark_magician = YugiohCard(
        name="Dark Magician",
        card_type="Monster",
        monster_type="Spellcaster",
        description="The ultimate wizard in terms of attack and defense.",
        attack=2500,
        defense=2000,
        attribute="Dark"
    )
    raigeki = YugiohCard(
        name="Raigeki",
        card_type="Spell",
        monster_type="-",
        description="Destroy all Monsters your opponent controls.",
        attack="-",
        defense="-",
        attribute="-"
    )
    mirror_force = YugiohCard(
        name="Mirror Force",
        card_type="Trap",
        monster_type="-",
        description="When an opponent's monster declares an attack: Destroy all your opponent's Attack Position monsters.",
        attack="-",
        defense="-",
        attribute="-"
    )

    db.execute(insert_SQL, (
        blue_eyes.name,
        blue_eyes.card_type,
        blue_eyes.monster_type,
        blue_eyes.description,
        blue_eyes.attack,
        blue_eyes.defense,
        blue_eyes.attribute,
    ))

    db.execute(insert_SQL, (
        dark_magician.name,
        dark_magician.card_type,
        dark_magician.monster_type,
        dark_magician.description,
        dark_magician.attack,
        dark_magician.defense,
        dark_magician.attribute,
    ))

    db.execute(insert_SQL, (
        raigeki.name,
        raigeki.card_type,
        raigeki.monster_type,
        raigeki.description,
        raigeki.attack,
        raigeki.defense,
        raigeki.attribute,
    ))

    db.execute(insert_SQL, (
        mirror_force.name,
        mirror_force.card_type,
        mirror_force.monster_type,
        mirror_force.description,
        mirror_force.attack,
        mirror_force.defense,
        mirror_force.attribute,
    ))

    db.execute("SELECT * FROM cards")
    print(f"Cards in table: {db.fetchall()}")
    db.execute("pragma table_list")
    results = db.fetchall()  # returns most recent command executed
    print(f"Results: {results}")