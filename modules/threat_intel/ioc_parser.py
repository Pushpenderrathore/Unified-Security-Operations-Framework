import re

def parse_ioc(value):
    if re.match(r"\d+\.\d+\.\d+\.\d+", value):
        return "ip"
    return "unknown"
