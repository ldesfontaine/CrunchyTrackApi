import os
from flask import Flask, request, jsonify, json
from datetime import datetime

app = Flask(__name__)

def isJson():
    try:
        if request.is_json:
            return  200
        else:
            return "Erreur 400: Requête incorrecte - Format JSON requis", 400
    except:
        return "Erreur interne du serveur", 500

def checkJsonFile():
    try:
        if not os.path.exists("save.json") or os.stat("save.json").st_size == 0:
            with open("save.json", "w") as file:
                file.write("{}")
            return "Fichier vérifié et initialisé", 200
        else:
            return "Fichier vérifié", 200
    except:
        raise ValueError("Erreur interne du serveur")

def get_data():
    global username, anime_title, episode_name, episode_number, episode_link
    data = request.get_json()

    # On récupère les infos nécessaires
    username = data["username"]
    anime_title = "Anime"
    episode_name = data["data"]["Anime"]["Title"]
    episode_number = data["data"]["Anime"]["EpisodeNumber"]
    episode_link = data["data"]["Anime"]["EpisodeLink"]

def write_data():
    try:
        data = request.get_json()
        if not data:
            return "Erreur 400: Requête incorrecte - Données JSON manquantes", 400

        # On récupère les infos nécessaires
        get_data()

        # Vérifier si le fichier save.json existe
        checkJsonFile()

        with open("save.json", "r+") as file:
            content = json.load(file)

            # Vérifier si l'utilisateur existe déjà dans le fichier
            if username in content:
                user_data = content[username]
            else:
                user_data = {}

            # Vérifier si l'anime title existe déjà pour cet utilisateur
            if anime_title in user_data:
                anime_data = user_data[anime_title]
            else:
                anime_data = {}

            # Mettre à jour les informations de l'épisode existant ou ajouter un nouvel épisode
            anime_data[episode_name] = {
                "EpisodeNumber": episode_number,
                "EpisodeLink": episode_link,
                "LastUpdate": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }

            # Mettre à jour les données de l'utilisateur dans le fichier
            user_data[anime_title] = anime_data
            content[username] = user_data

            # Réécrire le contenu du fichier avec les données mises à jour
            file.seek(0)
            file.truncate()
            json.dump(content, file, indent=4)

        return "Données enregistrées avec succès", 200

    except Exception as e:
        return "Erreur interne du serveur", 500


# ---------------------------------------------------Synchronisation---------------------------------------------------
@app.route('/save', methods=['POST'])
def save():
    try:
        isJson()
        checkJsonFile()
        write_data()
        return "Données enregistrées avec succès", 200
    except ValueError as e:
        return str(e), 400
    except Exception:
        return "Erreur interne du serveur", 500


if __name__ == '__main__':
    app.run()
