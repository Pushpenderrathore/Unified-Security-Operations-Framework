import json

KEYS = [
    r"Software\Microsoft\Windows\CurrentVersion\Run"
]

def capture_baseline(output="registry_baseline.json"):
    import winreg  # ✅ moved inside function

    snapshot = {}

    for key_path in KEYS:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                values = {}
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        values[name] = value
                        i += 1
                    except OSError:
                        break
                snapshot[key_path] = values
        except Exception:
            continue

    with open(output, "w") as f:
        json.dump(snapshot, f, indent=2)

    return snapshot

