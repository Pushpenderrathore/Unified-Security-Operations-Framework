def generate_report(alerts):
    return {
        "summary": {
            "suspicious_process_chains": len(alerts)
        },
        "alerts": alerts
    }
