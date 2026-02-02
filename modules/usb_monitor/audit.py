import datetime

def log_event(device_id, authorized):
    return {
        "device_id": device_id,
        "authorized": authorized,
        "status": "ALLOWED" if authorized else "BLOCKED",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

