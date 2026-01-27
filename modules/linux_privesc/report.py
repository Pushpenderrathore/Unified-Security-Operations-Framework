def generate_report(system, suid, sudo_rules, cron):
    report = {
        "system_info": system,
        "suid_binaries_count": len(suid),
        "dangerous_sudo": bool(sudo_rules),
        "writable_cron": cron
    }
    return report
