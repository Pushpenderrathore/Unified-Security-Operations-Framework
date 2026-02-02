def correlate(results):
    score = 0
    hits = 0
    for r in results:
        if r["malicious"]:
            hits += 1
            score += r["score"]
    return {
        "sources_flagged": hits,
        "avg_score": score // hits if hits else 0
    }

