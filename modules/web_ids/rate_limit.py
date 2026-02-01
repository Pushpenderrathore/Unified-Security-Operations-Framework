import time

REQUESTS = {}
LIMIT = 10

def allow(ip):
    now = time.time()
    REQUESTS.setdefault(ip, [])
    REQUESTS[ip] = [t for t in REQUESTS[ip] if now - t < 60]

    if len(REQUESTS[ip]) >= LIMIT:
        return False

    REQUESTS[ip].append(now)
    return True
