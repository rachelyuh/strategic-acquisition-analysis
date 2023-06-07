from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/results', methods = ["GET", "POST"])
def result():
    if request.method == "POST":
        file1 = open("file1.txt","r")
        line1 = file1.readline()
        props= {
        'percent': request.form['debt'],
        'buyer': line1[:4],
        'seller': line1[:-4]
        }
        file1.close()
        file1 = open("file1.txt","w")
        file1.truncate(0)
        file1.close()
        return render_template("results.html", props = props)
   
    
    return render_template("results.html", props = props)

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
        print(line)
        if (len(line) == 0):
            file1 = open("file1.txt","w")
            if (len(request.form['buyer']) != 4):
                return render_template("temp.html", new = True)
            file1.write(request.form['buyer'])
            file1.close()
            return render_template("temp.html", buyer = True, line = line)
        
        elif (len(line[0]) == 4):
            file1 = open("file1.txt","a")
            if (len(request.form['seller']) != 4):
                return render_template("temp.html", new = True)
            file1.write(request.form['seller'])
            file1.close()
            return render_template("temp.html", seller = True, line = line)
        
        
        else:

            return render_template("temp.html")
        
    
       
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)