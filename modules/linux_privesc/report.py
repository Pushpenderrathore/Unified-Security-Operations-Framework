def generate_report(system, suid_analysis, sudo_rules, cron):
    risk = "LOW"

    if suid_analysis["dangerous"]:
        risk = "HIGH"
    elif sudo_rules or cron:
        risk = "MEDIUM"

    return {
        "summary": {"risk_level": risk},
        "system_info": system,
        "suid": {
            "total": suid_analysis["total"],
            "dangerous_count": len(suid_analysis["dangerous"]),
            "dangerous_binaries": suid_analysis["dangerous"]
        },
        "dangerous_sudo": bool(sudo_rules),
        "writable_cron": cron
    }
