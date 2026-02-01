ATTACK_PATTERNS = {
    "SQLi": ["' OR 1=1", "UNION SELECT"],
    "XSS": ["<script>", "alert("],
    "LFI": ["../", "..\\"]
}

def detect_attack(request):
    findings = []
    for attack, patterns in ATTACK_PATTERNS.items():
        for p in patterns:
            if p.lower() in request.lower():
                findings.append(attack)
    return findings
