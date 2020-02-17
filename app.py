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
        except Exception as e:
            print(e)
            print(f"error transpiling {lines}")

    # Return the response in json format
    # origineel gebruikte we de eerste dat werkt opeens niet meer om
    # onduidelijke redenen! Het heeft vermoedelijk iets met strings en "" te maken
    # json_version_2 = jsonify(response) <- dit was het origineel
    # ook direct dumpen doet het niet
    # json_version = json.dump(response) <- ook foutmelding!
    # dus maken we er maar even met de hand geldige JSON van met str() Niet echt ideaal zo!!

    # er is trouwens niet eens perse JSON nodig we kunnen ook wel een string met
    # code passen

    print(repr(response))

    str_versie = str(response)
    str_versie = str_versie.replace("'Code'",'"Code"')
    return str_versie


# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# A welcome message to test our server
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
