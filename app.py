import ast
import json
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
import requests
import model
import company_info
import asyncio
import time
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# import jsonify
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)
@app.route('/history')
def history():
    token = oauth.auth0.authorize_access_token()
    user_info = oauth.auth0.parse_id_token(token)

    # Store user data in the session
    session['user'] = {
        'id': user_info['sub'],
        'name': user_info['name'],
        'email': user_info['email']
    }

    # Retrieve user data from the MongoDB collection
    user_data = users_collection.find_one({'user_id': user_info['sub']})

    if user_data:
        # User data exists in the collection
        return jsonify(user_data)
    else:
        # User data doesn't exist, you can choose to create a new record or handle accordingly
        return 'User data not found'

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/about', methods = ["GET"])
def about():
    return render_template("about.html")

@app.route('/loading', methods = ["GET", "POST"])
def loading():
    # Perform the database query here
    # ...
    if request.method == "POST":
        percent = request.form['debt']
        # Pass the query result to the loading template
        return render_template('loading.html', percent = percent)

@app.route('/fetch_data', methods = ["GET", "POST"])
def fetch_data():
    # Perform the database query here
    # ...
    
        file1 = open("file1.txt","r")
        line1 = file1.readline()
        text = line1.split(" ")
        buyer = text[0]
        seller = text[1]
        percent = request.args.get('percent')
        
        print(percent)
        
        file1.close()
        file1 = open("file1.txt","w")
        file1.truncate(0)
        file1.close()

        change_in_eps = model.change_in_yearly_eps(model.yearly_eps(buyer, seller, float(percent)))    

        file2 = open("file2.txt","w")
        file2.write(str(change_in_eps))
        file2.close()
    
        # Return the query result in JSON format
        return jsonify(change_in_eps)


@app.route('/results', methods = ["GET", "POST"])
def result():

        file2 = open("file2.txt","r")
        datavalue = file2.readline()

        file2.close()
        file2 = open("file2.txt","w")
        file2.truncate(0)
        file2.close()

        print(datavalue)
        return render_template("results.html", change_in_eps = ast.literal_eval(datavalue))


@app.route('/tutorial', methods = ["GET"])
def tutorial():
    return render_template("tutorial.html")

@app.route('/temp', methods = ["GET", "POST"])
def start():
    if request.method == "GET":
        file1 = open("file1.txt","w")
        file1.truncate(0)
        file1.close()

        return render_template("temp.html", new = True)
    else:
        file1 = open("file1.txt","r")
        line = file1.readlines()
        file1.close()
        if (len(line) == 0):
            file1 = open("file1.txt","w")
            file1.write(request.form['buyer'])
            file1.close()
            try:
                buyer_information = company_info.get_company_info(request.form['buyer'])
            except:
                file1 = open("file1.txt","w")
                file1.truncate(0)
                file1.close()
                return render_template("temp.html", new = True)
    
            return render_template("temp.html", buyer = True, line = line, buyer_information = buyer_information)
        
        elif (len(line[0]) == 2 or len(line[0]) == 3 or len(line[0]) == 4):
            file1 = open("file1.txt", "r")
            buyer_stock = file1.readline()
            file1.close()
            file1 = open("file1.txt","a")
            file1.write(" ")
            file1.write(request.form['seller'])
            file1.close()
            seller_stock = request.form['seller']
            try:
                buyer_information = company_info.get_company_info(buyer_stock)
                seller_information = company_info.get_company_info(seller_stock)
            except:
                file1 = open("file1.txt","w")
                file1.truncate(0)
                file1.close()
                return render_template("temp.html", new = True)
            return render_template("temp.html", seller = True, line = line, buyer_information = buyer_information, seller_information = seller_information)
        
        
        else:

            return render_template("temp.html")
        
    
       
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)