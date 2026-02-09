import os
import json
import datetime

KEYS = [
    r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
    r"Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce"
]

BASELINE_FILE = "data/registry_baseline.json"


def snapshot_registry():
    import winreg  # ✅ moved inside function (CRITICAL)

    data = {}
    for key_path in KEYS:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as k:
                values = {}
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(k, i)
                        values[name] = value
                        i += 1
                    except OSError:
                        break
                data[key_path] = values
        except Exception:
            data[key_path] = {}
    return data


def monitor_registry():
    if os.name != "nt":
        raise RuntimeError("Windows only")  # ✅ runtime check, CI-safe

    old = {}
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE) as f:
            old = json.load(f)

    current = snapshot_registry()

    changes = []
    for key in current:
        old_vals = old.get(key, {})
        new_vals = current[key]

        for v in new_vals:
            if v not in old_vals:
                changes.append({
                    "key": key,
                    "value": v,
                    "data": new_vals[v],
                    "change": "ADDED"
                })

        for v in old_vals:
            if v not in new_vals:
                changes.append({
                    "key": key,
                    "value": v,
                    "change": "REMOVED"
                })

    with open(BASELINE_FILE, "w") as f:
        json.dump(current, f, indent=2)

    return {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "changes": changes,
        "total_changes": len(changes)
    }

