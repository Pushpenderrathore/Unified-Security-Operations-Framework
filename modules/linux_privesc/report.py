def generate_report(system, suid, sudo_rules, cron):
    return {
        "summary": {
            "risk_level": "LOW" if not suid and not sudo_rules and not cron else "REVIEW REQUIRED"
        },
        "system_info": system,
        "suid_binaries_count": len(suid),
        "dangerous_sudo": bool(sudo_rules),
        "writable_cron": cron
    }
