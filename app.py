from flask import Flask, render_template, request, url_for, redirect, session
import requests
import model
import company_info
import asyncio
import time
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

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
# @app.route('/loading', methods = ["GET", "POST"])
# def loading():
#     # Perform the database query here
#     # ...
#     percent = request.form['debt']
#     # Pass the query result to the loading template
#     return render_template('loading.html', percent = percent)

# @app.route('/fetch_data', methods = ["GET", "POST"])
# def fetch_data():
#     # Perform the database query here
#     # ...
#     file1 = open("file1.txt","r")
#     line1 = file1.readline()
#     percent = request.form['debt']
#     text = line1.split(" ")
#     buyer = text[0]
#     seller = text[1]
    
#     file1.close()
#     file1 = open("file1.txt","w")
#     file1.truncate(0)
#     file1.close()

#     change_in_eps = model.change_in_yearly_eps(model.yearly_eps(buyer, seller, float(percent)))    
#     # Return the query result in JSON format
#     return change_in_eps


@app.route('/results', methods = ["GET", "POST"])
async def result():
    if request.method == "POST":

        file1 = open("file1.txt","r")
        line1 = file1.readline()
        percent = request.form['debt']
        text = line1.split(" ")
        buyer = text[0]
        seller = text[1]
        
        file1.close()
        file1 = open("file1.txt","w")
        file1.truncate(0)
        file1.close()


        change_in_eps = model.change_in_yearly_eps(model.yearly_eps(buyer, seller, float(percent)))        
        # change_in_eps = request.form['data']
        return render_template("results.html", change_in_eps = change_in_eps)

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
            if (len(request.form['buyer']) != 4):
                return render_template("temp.html", new = True)
            file1.write(request.form['buyer'])
            file1.close()
            buyer_information = company_info.get_company_info(request.form['buyer'])
    
            return render_template("temp.html", buyer = True, line = line, buyer_information = buyer_information)
        
        elif (len(line[0]) == 2 or len(line[0]) == 3 or len(line[0]) == 4):
            file1 = open("file1.txt", "r")
            buyer_stock = file1.readline()
            file1.close()
            file1 = open("file1.txt","a")
            if (len(request.form['seller']) != 4):
                return render_template("temp.html", new = True)
            file1.write(" ")
            file1.write(request.form['seller'])
            file1.close()
            seller_stock = request.form['seller']
            buyer_information = company_info.get_company_info(buyer_stock)
            seller_information = company_info.get_company_info(seller_stock)
            return render_template("temp.html", seller = True, line = line, buyer_information = buyer_information, seller_information = seller_information)
        
        
        else:

            return render_template("temp.html")
        
    
       
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)