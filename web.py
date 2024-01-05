from flask import Flask

app = Flask("Web")

@app.route("/")
def home():
  return "V2Writer"