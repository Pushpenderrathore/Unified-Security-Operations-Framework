def normalize(feed_name, raw):
    return {
        "source": feed_name,
        "malicious": raw.get("abuseConfidenceScore", 0) > 50,
        "score": raw.get("abuseConfidenceScore", 0)
    }

