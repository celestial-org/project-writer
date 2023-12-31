from flask import flask

app = Flask("Web")

@app.route("/")
def home():
  return "V2Writer"