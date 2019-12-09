import hedy

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
        response["Code"] = hedy.transpile(lines)

    # Return the response in json format
    return jsonify(response)


# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# A welcome message to test our server
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)