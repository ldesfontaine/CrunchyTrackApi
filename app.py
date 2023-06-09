import os
from flask import Flask, request, json
from datetime import datetime

app = Flask(__name__)


# ---------------------------------------------------Synchronisation---------------------------------------------------
@app.route('/save', methods=['POST'])
def save_data():
    try:
        get_data()
        checkFile()
        # write_data()
        return data_with_timestamp, 200
    except:
        return "Error 400: Bad Request"



def get_data():
    global data_with_timestamp
    try:
        data = request.get_json()
        data_without_name = data["data"]
        data_with_timestamp = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "username": data["username"],
            "data": data_without_name}
        return data_with_timestamp, 200
    except:
        return "Error 400: Bad Request"


def checkFile():
    if not os.path.exists("save.json"):
        with open("save.json", "w") as file:
            file.write("")
    return "File checked"

# def write_data():
    #         users = [user["username"] for user in data]
    #         if data_with_timestamp["username"] in users:
    #             index = users.index(data_with_timestamp["username"])
    #             data[index]["data"].append(data_with_timestamp["data"])
    #         else:
    #             data.append(data_with_timestamp)
    #     with open("save.json", "w") as file:
    #         json.dump(data, file)
    #     return "Data written", 200
    # except:
    #     return "Error 400: Bad Request"



if __name__ == '__main__':
    app.run()
