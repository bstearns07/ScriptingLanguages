# import the main Flask object
from flask import Flask
import os
import swimclub

# create a flask object for the app
# use the dunder name to associate the web app with the code's current namespace as required by Flask
app = Flask(__name__)

# use @ decorator to associate get requests for the "/" url with the following index function
@app.get("/")
def index():
    return "This is a placeholder for your webapp's opening page."

# define a function to handle GET requests for /swimmers url's
# returns an ordered list of each swimmer
@app.get("/swimmers")
def display_swimmers():
    swim_files = os.listdir("swimdata")
    if ".DS_Store" in swim_files:
        swim_files.remove(".DS_Store")
    swimmers = []
    for file in swim_files:
        name, *_ = swimclub.Read_Swim_Data(file)
        if name not in swimmers:
            swimmers.append(name)
    # cast results to a string to ensure data sent to the browser is text as it expects
    return str(sorted(swimmers))

# define a function to handle /files/<swimmer> get requests to return a swimmers files
@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    return str(swimmers[swimmer])

if __name__ == "__main__":
    # run Flasks built-in web server and pass the web app code to it
    # run in debugging mode: Flask watches to saved changes in code and restarts the app automatically
    app.run(debug=True)