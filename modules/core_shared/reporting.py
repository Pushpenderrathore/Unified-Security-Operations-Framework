import json
import datetime

def generate_base_report(module, summary, data):
    return {
        "module": module,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "summary": summary,
        "data": data
    }

def save_report(report, path):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
