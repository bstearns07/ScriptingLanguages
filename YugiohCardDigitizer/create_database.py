from Yugioh_Card import YugiohCard
import sqlite3
import DBcm

db_details ="Cards.sqlite3"
insert_SQL = """
    INSERT INTO cards (name, attack, defense, description, type, color)
    VALUES (?, ?, ?, ?, ?, ?)
"""

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
        card_type="Monster",
        monster_type="Dragon",
        attribute="Light"
    )
    dark_magician = YugiohCard(
        name="Dark Magician",
        description="The ultimate wizard in terms of attack and defense.",
        attack=2500,
        defense=2000,
        monster_type="Spellcaster",
        card_type="Monster",
        attribute="Dark"
    )
    raigeki = YugiohCard(
        name="Raigeki",
        description="Destroy all Monsters you opponent controls.",
        card_type="Spell",
        attack="-",
        defense="-",
        monster_type="-"
    )
    mirror_force = YugiohCard(
        name="Mirror Force",
        description="When an opponent's monster declares an attack: Destroy all your opponent's Attack Position monsters.",
        card_type="Trap",
        attack="-",
        defense="-",
        monster_type="-"
    )

    db.execute(insert_SQL, (
        blue_eyes.name,
        blue_eyes.attack,
        blue_eyes.defense,
        blue_eyes.description,
        blue_eyes.attribute,
        blue_eyes.card_type
    ))

    db.execute(insert_SQL, (
        dark_magician.name,
        dark_magician.attack,
        dark_magician.defense,
        dark_magician.description,
        dark_magician.attribute,
        dark_magician.card_type
    ))

    db.execute(insert_SQL, (
        raigeki.name,
        raigeki.description,
        raigeki.card_type,
        raigeki.attribute,
        raigeki.attack,
        raigeki.defense
    ))

    db.execute(insert_SQL, (
        mirror_force.name,
        mirror_force.description,
        mirror_force.card_type,
        mirror_force.attribute,
        mirror_force.attack,
        mirror_force.defense
    ))

    db.execute("SELECT * FROM cards")
    print(f"Cards in table: {db.fetchall()}")
    db.execute("pragma table_list")
    results = db.fetchall()  # returns most recent command executed
    print(f"Results: {results}")