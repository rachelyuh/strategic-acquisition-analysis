from flask import Flask, render_template, request
import requests
import model
import company_info
app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/results', methods = ["GET", "POST"])
def result():
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