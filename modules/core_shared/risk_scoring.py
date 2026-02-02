def score_from_flags(flags: dict):
    score = 0
    for k, v in flags.items():
        if v:
            score += 10
    return min(score, 100)

def risk_level(score):
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"
