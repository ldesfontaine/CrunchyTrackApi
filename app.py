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

def isExist():
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
    global data
    data = request.get_json()

def write_data():
    try:
        data = request.get_json()
        if not data:
            return "Erreur 400: Requête incorrecte - Données JSON manquantes", 400

        # On récupère les infos nécessaires
        get_data()

        # Vérifier si le fichier save.json existe
        isExist()

        with open("save.json", "r+", encoding='utf-8') as file:
            content = json.load(file)

            for entry in data["data"]:
                anime_title = entry["Anime"]["Title"]
                episode_name = entry["Anime"]["EpisodeName"]
                episode_number = entry["Anime"]["EpisodeNumber"]
                episode_link = entry["Anime"]["EpisodeLink"]

                # Vérifie si l'utilisateur existe déjà
                if data["username"] in content:
                    user_data = content[data["username"]]
                else:
                    user_data = {}

                # Vérifie si l'anime title existe déjà pour cet user
                if anime_title in user_data:
                    anime_data = user_data[anime_title]
                else:
                    anime_data = {}

                # Update les informations de l'épisode existant ou ajouter un nouvel épisode avec heure de mise à jour
                anime_data[episode_name] = {
                    "EpisodeNumber": episode_number,
                    "EpisodeLink": episode_link,
                    "LastUpdate": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }

                # Mets à jour les données de l'utilisateur
                user_data[anime_title] = anime_data
                content[data["username"]] = user_data

            # Réécrire le contenu du fichier avec les données mises à jour
            file.seek(0)
            file.truncate()
            json.dump(content, file, ensure_ascii=False, indent=4)

        return "Données enregistrées avec succès", 200

    except Exception as e:
        return "Erreur interne du serveur", 500


# ---------------------------------------------------Synchronisation---------------------------------------------------
@app.route('/save', methods=['POST'])
def save():
    try:
        isJson()
        write_data()
        return "Données enregistrées avec succès", 200
    except ValueError as e:
        return str(e), 400
    except Exception:
        return "Erreur interne du serveur", 500


if __name__ == '__main__':
    app.run()
