import time

WINDOW = 60
LIMIT = 20
BUCKET = {}


def allow(ip):
    now = time.time()
    BUCKET.setdefault(ip, [])
    BUCKET[ip] = [t for t in BUCKET[ip] if now - t < WINDOW]

    if len(BUCKET[ip]) >= LIMIT:
        return False

    BUCKET[ip].append(now)
    return True

