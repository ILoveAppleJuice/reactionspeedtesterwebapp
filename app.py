from flask import Flask,render_template,redirect,request,jsonify
import random
import json
from datetime import datetime

# load data from json
with open('data.json', 'r') as file:
    data:list = json.load(file)

def SaveData():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

colorPool = [
    {
        "ColorName":"Red",
        "Hex":"#ff0000"
    },
    {
        "ColorName":"Yellow",
        "Hex":"#ffff00"
    },
    {
        "ColorName":"Blue",
        "Hex":"#0000ff"
    },
    {
        "ColorName":"Green",
        "Hex":"#00ff00"
    }
]

def GetRandomColor():
    color = colorPool[random.randint(0,len(colorPool)-1)]
    return color

def ProcessData(data):
    new = {
        "SubjectInfo":{
            "grade":data["SubjectInfo"]["grade"],
            "gender":data["SubjectInfo"]["gender"],
            "sports":[]
        },
        "Results":data["Results"],
        "Timestamp":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }

    for k,v in data["SubjectInfo"].items():
        if v == "on":
            new["SubjectInfo"]["sports"].append(k)
        if k == "sportsOther" and v != "":
            new["SubjectInfo"]["sports"].append(v)
        print(k,v)

    return new

@app.route("/")
def index():
    print(request)
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/completed")
def completed():
    return render_template("completed.html")

@app.route("/api/submit",methods=["POST"])
def handleSubmitRequest():
    requestData = request.get_json()
    processedData = ProcessData(requestData)
    data.append(processedData)
    print(processedData)
    SaveData()
    
    return "200"

@app.route("/api/data",methods=["GET"])
def handleGetDataRequest():
    return jsonify(data)

@app.route("/api/getColor",methods=["GET"])
def handleGetColorRequest():
    return jsonify(GetRandomColor())



if __name__ == "__main__":
    app.run(host="0.0.0.0",port="80",debug=True)