import re

def parse_ioc(value):
    if re.match(r"\d+\.\d+\.\d+\.\d+", value):
        return "ip"
    if "." in value:
        return "domain"
    return "unknown"

