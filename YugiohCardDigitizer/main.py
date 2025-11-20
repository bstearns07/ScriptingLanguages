from flask import Flask, session, render_template, request
import webbrowser

# create a flask object for the app
# use the dunder name to associate the web app with the code's current namespace as required by Flask
app = Flask(__name__)
# enable app to work with session by creating a key that flask uses to encrypt cookies sent to browser
app.secret_key = "supersecretcantguessme"

@app.get("/")
def index():
    # imports a html file stored in the "templates" folder
    return render_template(
        "index.html",
        title="Yugioh Card Digitizer",)

# define a function for handling requests to view the library
@app.get("/library")
def library():
    return render_template(
        "library.html",
        title="Yugioh Card Library",
    )

# if the program is run directly, open the app in a web browser and run the app
if __name__ == "__main__":
    # run Flask's built-in web server and pass the web app code to it
    # run in debugging mode: Flask watches to saved changes in code and restarts the app automatically
    webbrowser.open("http://127.0.0.1:8000")
    app.run(debug=True, port=8000)