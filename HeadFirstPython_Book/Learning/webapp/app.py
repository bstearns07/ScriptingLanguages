# import the main Flask object
from flask import Flask, session, render_template, request
import os
import swimclub

# create a flask object for the app
# use the dunder name to associate the web app with the code's current namespace as required by Flask
app = Flask(__name__)
# enable app to work with session by creating a key that flask uses to encrypt cookies sent to browser
app.secret_key = "supersecretcantguessme"

# use @ decorator to associate get requests for the "/" url with the following index function
@app.get("/")
def index():
    # imports a html file stored in the "templates" folder
    return render_template(
        "index.html",
        title="Welcome to the Swimclub system",)

# define a function to populate a session dictionary of swimmers files
def populate_data():
    if "swimmers" not in session:
        swim_files = os.listdir("swimdata")
        if ".DS_Store" in swim_files:
            swim_files.remove(".DS_Store")
        session["swimmers"] = {}
        for file in swim_files:
            name, *_ = swimclub.Read_Swim_Data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []
            session["swimmers"][name].append(file)
# define a function to handle GET requests for /swimmers url's
# returns an ordered list of each swimmer
@app.get("/swimmers")
def display_swimmers():
    populate_data()
    # cast results to a string to ensure data sent to the browser is text as it expects
    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showfiles",
        select_id="swimmer",
        data=sorted(session["swimmers"])
    )

# define a function to handle /files/<swimmer> get requests to return a swimmers files
@app.post("/showfiles")
def get_swimmers_files():
    populate_data()
    name = request.form["swimmer"]
    return render_template(
        "select.html",
        title="Select an event",
        select_id="file",
        url="/showbarchart",
        data=session["swimmers"][name]
    )

# define function for /showbarchart post requests
@app.post("/showbarchart")
def show_bar_chart():
    file_id = request.form["file"] # returns the filename selected from the /showfiles select element
    # use the produce_bar_chart function to create a save a html file for the file_id's bar chart to /templates folder
    # use render_template to then load that saved html file (must remove templates/ suffix. Jinja looks for HTML files)
    location = swimclub.produce_bar_chart(file_id,"templates/")
    return render_template(location.split("/")[-1])


if __name__ == "__main__":
    # run Flasks built-in web server and pass the web app code to it
    # run in debugging mode: Flask watches to saved changes in code and restarts the app automatically
    app.run(debug=True, port=8080)