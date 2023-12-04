from flask import Flask, request, jsonify

app = Flask('')


@app.route('/', methods=["GET", "POST"])
def main():
  if request.method == "POST":
    try:
      return jsonify(request.get_data())
    except:
      return request.get_data()
  else:
    return "Hello, World!"
