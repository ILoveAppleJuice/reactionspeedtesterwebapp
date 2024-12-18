from flask import Flask,render_template,redirect,request

app = Flask(__name__)


app.route("/")
def index():
    ...

app.route("/api/submit",methods=["POST"])
def handleSubmitRequest():
    ...

app.route("/api/data",methods=["GET"])
def handleGetDataRequest():
    ...

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="80",debug=True)