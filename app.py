from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    response = requests.get("https://financialmodelingprep.com/api/v3/income-statement/AAPL?limit=120&apikey=4975d0effdd49277f9f496ce27032830")
    return response.json()

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)