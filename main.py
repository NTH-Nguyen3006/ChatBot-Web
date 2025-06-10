from flask import Flask, request, jsonify, render_template, redirect
from app import generate_Content

_app = Flask(__name__)
_app.template_folder = "templates"
_app.static_folder = "static"

@_app.route("/", methods = ["GET"])
def home():
    return render_template("home.html")

@_app.route("/introduction", methods = ["GET"])
def introduction():
    return render_template("introduction.html")

@_app.route("/bot", methods = ["POST"])
def botController():
    req: dict = request.get_json()
    message = req.get("message", None)
    attchment = req.get('attchment', None)
    response = generate_Content(prompt=message, attchment=attchment)
    
    return jsonify({
        "model": response
    }), 200


if __name__ == "__main__":
    _app.run(host="localhost", port=8080, debug=True)
    