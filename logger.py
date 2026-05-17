import json
from datetime import datetime

def log_activity(message):
    log = {
        "time": str(datetime.now()),
        "message": message
    }

    try:
        with open("data/logs.json") as f:
            data = json.load(f)
    except:
        data = []

    data.append(log)

    with open("data/logs.json", "w") as f:
        json.dump(data, f, indent=4)
        