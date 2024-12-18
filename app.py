from flask import Flask,render_template,redirect,request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

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
    ...

@app.route("/api/data",methods=["GET"])
def handleGetDataRequest():
    ...

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="80",debug=True)