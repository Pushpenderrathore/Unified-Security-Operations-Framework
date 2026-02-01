def generate_blocklist(ioc, correlation):
    if correlation["sources_flagged"] >= 1:
        return {"ioc": ioc, "action": "BLOCK"}
    return {"ioc": ioc, "action": "ALLOW"}

