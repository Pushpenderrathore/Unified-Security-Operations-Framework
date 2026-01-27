def calculate_risk(data):
    score = data["data"].get("abuseConfidenceScore", 0)

    if score >= 80:
        return "HIGH RISK"
    elif score >= 40:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"
