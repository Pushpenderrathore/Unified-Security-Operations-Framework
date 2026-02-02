def generate_report(events):
    unauthorized = [e for e in events if e["status"] == "BLOCKED"]

    return {
        "total_events": len(events),
        "unauthorized_devices": len(unauthorized),
        "events": events
    }

