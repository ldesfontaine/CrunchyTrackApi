import os
from flask import Flask, request, json
from datetime import datetime

app = Flask(__name__)


# ---------------------------------------------------Synchronisation---------------------------------------------------
@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        username = data.get("username")  # Récupérer le nom d'utilisateur depuis les données reçues
        data_with_timestamp = {
            "timestamp": timestamp,
            "username": username,
            "data": data
        }
        if os.path.exists("save.json"):
            with open("save.json", "a") as f:
                f.write(json.dumps(data_with_timestamp,indent=4))
        else:
            with open("save.json", "w") as f:
                f.write(json.dumps(data_with_timestamp,indent=4))
        return "OK", 200
    except:
        return "404", 404


# ---------------------------------------------------ListJSON---------------------------------------------------
@app.route('/list', methods=['GET'])
def list_data():
    # Si le fichier save.json existe, on le lit et on renvoie son contenu
    if os.path.exists("save.json"):
        with open("save.json", "r") as f:
            return json.dumps(f.read()), 200
    else:
        return "404", 404


# ---------------------------------------------------GetJSONByUsername---------------------------------------------------
@app.route('/get/<username>', methods=['GET'])
def get_data(username):
    # Si le fichier save.json existe, on le lit et on renvoie les données correspondant au nom d'utilisateur
    if os.path.exists("save.json"):
        with open("save.json", "r") as f:
            for line in f:
                data_with_timestamp = json.loads(line)
                if data_with_timestamp["username"] == username:
                    return json.dumps(data_with_timestamp["data"]), 200
            return "404", 404
    else:
        return "404", 404


if __name__ == '__main__':
    app.run()
