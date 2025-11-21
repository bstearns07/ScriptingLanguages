import os

from flask import Flask, session, render_template, request, redirect
import webbrowser
import DBcm

# create a flask object for the app
# use the dunder name to associate the web app with the code's current namespace as required by Flask
app = Flask(__name__)
# enable app to work with session by creating a key that flask uses to encrypt cookies sent to browser
app.secret_key = "supersecretcantguessme"

# define function for retrieving all cards in the database and storing in session
def retrieve_library():
    db_details = "Cards.sqlite3"

    # 1. Check if data in session is still valid
    with DBcm.UseDatabase(db_details) as db:
        db.execute("SELECT MAX(id) FROM cards")
        latest_id = db.fetchone()[0]

    # If session has no cache or database changed → refresh cache
    if "cards" not in session or session.get("cards_latest_id") != latest_id:
        with DBcm.UseDatabase(db_details) as db:
            SQL = """
                SELECT id, name, card_type, monster_type, description, attack, defense, attribute
                FROM cards
                ORDER BY id
            """
            db.execute(SQL)
            results = db.fetchall()

        # Convert tuples to list of dictionaries for easier Jinja display
        cards = []
        for row in results:
            cards.append({
                "id": row[0],
                "name": row[1],
                "card_type": row[2],
                "monster_type": row[3],
                "description": row[4],
                "attack": row[5],
                "defense": row[6],
                "attribute": row[7],
            })

        # Save new cache + new database state
        session["cards"] = cards
        session["cards_latest_id"] = latest_id

    return session["cards"]

@app.get("/")
def index():
    # imports a html file stored in the "templates" folder
    return render_template(
        "index.html",
        title="Yugioh Card Digitizer",)

# define a function for handling requests to view the library
@app.get("/library")
def library():
    cards = retrieve_library()
    return render_template(
        "library.html",
        title="Your Library",
        cards=cards
    )

# define a function to handle get requests to view a card's details
@app.get("/view/<int:card_id>")
def view_card(card_id):
    db_details = "Cards.sqlite3"
    with DBcm.UseDatabase(db_details) as db:
        query = "SELECT * FROM cards WHERE id = ?"
        db.execute(query, (card_id,))
        card = db.fetchone()
    return render_template("view_card.html", card=card)

# define a function for handling get requests for editing a card in the database
@app.route("/edit/<int:card_id>", methods=["GET", "POST"])
def edit_card(card_id):
    db_details = "Cards.sqlite3"

    # GET → load the form with card data
    if request.method == "GET":
        cards = retrieve_library()
        card = next((c for c in cards if c["id"] == card_id), None)

        if card is None:
            return "Card not found", 404

        return render_template(
            "add_edit.html",
            title="Edit Card",
            card=card
        )

    # POST → save the updated card
    form = request.form
    with DBcm.UseDatabase(db_details) as db:
        SQL = """
            UPDATE cards
            SET name=?, card_type=?, monster_type=?, description=?, attack=?, defense=?, attribute=?
            WHERE id=?
        """
        db.execute(SQL, (
            form["name"],
            form["card_type"],
            form["monster_type"],
            form["description"],
            form["attack"],
            form["defense"],
            form["attribute"],
            card_id
        ))

    # Clear the cached library so it refreshes
    session.pop("cards", None)

    return redirect("/library")

# define a function for handling POST requests for posting updated information of a card to the database
@app.post("/add")
def add_card_post():
    db_details = "Cards.sqlite3"
    form = request.form

    with DBcm.UseDatabase(db_details) as db:
        SQL = """
            INSERT INTO cards (name, card_type, monster_type, description, attack, defense, attribute)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db.execute(SQL, (
            form["name"],
            form["card_type"],
            form["monster_type"],
            form["description"],
            form["attack"],
            form["defense"],
            form["attribute"]
        ))

    # Clear session cache
    session.pop("cards", None)

    return redirect("/library")

# define function for handling requests to add a new card to the database
@app.get("/add")
def add_card():
    return render_template(
        "add_edit.html",
        title="Add Card",
        card=None  # no card = adding mode
    )

# defines a function for handling get requests to confirm deletion before deleting a card from the database
@app.get("/delete/<int:card_id>")
def confirm_delete(card_id):
    db_details = "Cards.sqlite3"

    with DBcm.UseDatabase(db_details) as db:
        SQL = "SELECT id, name, image_filename FROM cards WHERE id = ?"
        db.execute(SQL, (card_id,))
        card = db.fetchone()

    if not card:
        return redirect("/library")

    card_obj = {
        "id": card[0],
        "name": card[1],
        "image_filename": card[2]
    }

    return render_template("confirm_delete.html", card=card_obj)

# define a functon to handle post request to delete a card from tbe database
@app.post("/delete/<int:card_id>")
def delete_card(card_id):
    db_details = "Cards.sqlite3"

    with DBcm.UseDatabase(db_details) as db:
        SQL = "SELECT image_filename FROM cards WHERE id = ?"
        db.execute(SQL, (card_id,))
        row = db.fetchone()

        SQL = "DELETE FROM cards WHERE id = ?"
        db.execute(SQL, (card_id,))

    # Clear cached session list if you use one
    session.pop("cards", None)

    # Delete image file if present
    if row and row[0]:
        filepath = os.path.join("static", "images", "cards", row[0])
        if os.path.exists(filepath):
            os.remove(filepath)

    return redirect("/library")

# if the program is run directly, open the app in a web browser and run the app
if __name__ == "__main__":
    # run Flask's built-in web server and pass the web app code to it
    # run in debugging mode: Flask watches to saved changes in code and restarts the app automatically
    webbrowser.open("http://127.0.0.1:8000")
    app.run(debug=True, port=8000)