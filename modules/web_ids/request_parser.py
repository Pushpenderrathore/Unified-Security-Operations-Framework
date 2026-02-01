def parse_request(raw):
    return {
        "request": raw,
        "length": len(raw)
    }
