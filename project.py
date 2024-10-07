from flask import *
import datetime
import hashlib
from db import MongoDBHelper
from bson.objectid import ObjectId

web_app = Flask("Flipazon")
db_helper = MongoDBHelper()

@web_app.route("/") #Decorator
def signup():
    return render_template("signup.html")

@web_app.route("/login")
def register():
    return render_template("login.html")

@web_app.route("/home")
def home():
    return render_template("home.html")

@web_app.route("/add-user", methods= ["POST"])
def add_user_in_db():
    # Create Dictionary with data from HTML form
    user_data = {
        "email": request.form["email"],
        "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest(),
        "created_on": datetime.datetime.now()
    }
    db_helper.collection = db_helper.db["users"]
    # To save Data in MongoDB
    result = db_helper.insert(user_data)
    #message = "User Id is {}".format(result.inserted_id)
    #return message

    # Write the data in the Session Object
    # This data can be used anywhere in the project
    session['user_id'] = str(result.inserted_id)
    session['email'] = user_data["email"]

    return render_template("home.html")

@web_app.route("/fetch-user", methods= ["POST"])
def fetch_user_from_db():
   
    
    # Create Dictionary with data from HTML form
    user_data = {
        "email": request.form["email"],
        "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest()
    }
    db_helper.collection = db_helper.db["users"]
    # To fetch Data from MongoDB
    result = db_helper.fetch(query = user_data)

    if len(result)>0:
        user_data = result[0]
        session['email'] = user_data["email"]

        return render_template("home.html")
    else:
        return render_template("error.html", message ="User Not Found. Please Try Again")
   

def main():
    # To use Session Tracking, create a secret key
    web_app.secret_key = "flipazon-key-v1"
    # App will run Infinitely, until user quits
    web_app.run(debug = True)
    #web_app.run(port = 5001) #optionally you can give port number

if __name__ == "__main__":
    main()