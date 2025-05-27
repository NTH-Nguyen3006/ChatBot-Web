from flask import Flask, request, jsonify, render_template
from bot import *

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

@app.route("/", methods = ["GET"])
def home():
    return render_template("home.html")

@app.route("/introduction", methods = ["GET"])
def introduction():
    return render_template("introduction.html")

@app.route("/bot", methods = ["POST"])
def botController():
    
    
    return jsonify({
        "model": r""""""
    }), 200



if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)