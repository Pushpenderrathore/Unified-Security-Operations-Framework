def generate_report(findings):
    return {
        "alerts": findings,
        "total": len(findings)
    }
