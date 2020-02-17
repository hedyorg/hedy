import hedy
import json

# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__, static_url_path='')

@app.route('/parse/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    lines = request.args.get("code", None)

    # For debugging
    print(f"got code {lines}")

    response = {}

    # Check if user sent code
    if not lines:
        response["Error"] = "no code found, please send code."
    # is so, parse
    else:
        try:
            result = hedy.transpile(lines)
            response["Code"] = result
        except Exception as E:
            print(f"error transpiling {lines}")
            response["Error"] = str(E)

    return jsonify(response)


# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# routing to index.html
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)