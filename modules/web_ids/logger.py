import datetime

LOGS = []

def log(ip, attack):
    entry = {
        "ip": ip,
        "attack": attack,
        "time": datetime.datetime.utcnow().isoformat() + "Z"
    }
    LOGS.append(entry)
    return entry

