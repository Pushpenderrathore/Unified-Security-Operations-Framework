import json

ALLOWLIST_FILE = "data/usb_allowlist.json"

def load_allowlist():
    try:
        with open(ALLOWLIST_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def is_authorized(device_id):
    allowlist = load_allowlist()
    return device_id in allowlist
