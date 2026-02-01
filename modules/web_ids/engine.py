from .rules import detect_attack
from .rate_limit import allow
from .logger import log

def inspect(ip, payload):
    findings = detect_attack(payload)
    allowed = allow(ip)

    logs = []
    for f in findings:
        logs.append(log(ip, f))

    return {
        "rate_allowed": allowed,
        "alerts": logs
    }

