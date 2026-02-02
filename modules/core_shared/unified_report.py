import datetime

def unify(reports: dict):
    return {
        "soc_framework": "Unified-SOC",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "modules": reports
    }

