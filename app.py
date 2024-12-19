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
            "gaming":data["SubjectInfo"]["gaming"],
            "sports":[]
        },
        "Color":data["Color"],
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

@app.route("/data",methods=["GET"])
def handleGetDataRequest():
    return jsonify(data)

@app.route("/api/getColor",methods=["GET"])
def handleGetColorRequest():
    return jsonify(GetRandomColor())

@app.route("/api/getColors",methods=["GET"]) # (with an "s")
def handleGetColorsRequest():
    return jsonify(colorPool)



@app.route("/stats",methods=["GET"])
def handleGetStatsRequest():
    stats = {
        "Color" : {},
        "Gender" : {},
        "Grade": {},
    }

    for i in range(len(data)):
        result = data[i]
        colorName = result["Color"]
        stats["Color"][colorName] = stats["Color"].get(colorName) or {"Average":0,"Times":[]}
        stats["Color"][colorName]["Times"].append(result["Results"])

    #bruh
    for i in range(len(data)):
        result = data[i]
        gender = result["SubjectInfo"]["gender"]
        stats["Gender"][gender] = stats["Gender"].get(gender) or {"Average":0,"Times":[]}
        stats["Gender"][gender]["Times"].append(result["Results"])

    #bruh
    for i in range(len(data)):
        result = data[i]
        grade = result["SubjectInfo"]["grade"]
        stats["Grade"][grade] = stats["Grade"].get(grade) or {"Average":0,"Times":[]}
        stats["Grade"][grade]["Times"].append(result["Results"])

    
    for _,jit in stats.items():
        for i,category in jit.items():
            category["Average"] = sum([sum(t)/len(t) for t in category["Times"]])/len(category["Times"])
            


    return jsonify(stats)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port="80",debug=True)