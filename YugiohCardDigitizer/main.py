from flask import Flask, session, render_template, request
import webbrowser
import DBcm

# create a flask object for the app
# use the dunder name to associate the web app with the code's current namespace as required by Flask
app = Flask(__name__)
# enable app to work with session by creating a key that flask uses to encrypt cookies sent to browser
app.secret_key = "supersecretcantguessme"

# define function for retrieving all cards in the database and storing in session
def retrieve_library(force_refresh=False):
    db_details = "Cards.sqlite3"

    # Only hit the database if necessary
    if not force_refresh and "cards" in session:
        return session["cards"]

    """Retrieve all cards from the database and store them in the session."""
    with DBcm.UseDatabase(db_details) as db:
        SQL = """SELECT id, name, card_type, monster_type, description, attack, defense, attribute
                 FROM cards"""
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

    # Store in session
    session["cards"] = cards
    return cards

@app.get("/")
def index():
    # imports a html file stored in the "templates" folder
    return render_template(
        "index.html",
        title="Yugioh Card Digitizer",)

# define a function for handling requests to view the library
@app.get("/library")
def library():
    cards = retrieve_library(force_refresh=True)
    return render_template(
        "library.html",
        title="Your Library",
        cards=cards
    )

# if the program is run directly, open the app in a web browser and run the app
if __name__ == "__main__":
    # run Flask's built-in web server and pass the web app code to it
    # run in debugging mode: Flask watches to saved changes in code and restarts the app automatically
    webbrowser.open("http://127.0.0.1:8000")
    app.run(debug=True, port=8000)