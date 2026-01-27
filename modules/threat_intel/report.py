def generate_report(ioc, data, risk):
    return {
        "ioc": ioc,
        "source": "AbuseIPDB",
        "abuse_confidence_score": data["data"].get("abuseConfidenceScore"),
        "country": data["data"].get("countryCode"),
        "isp": data["data"].get("isp"),
        "risk_level": risk
    }
