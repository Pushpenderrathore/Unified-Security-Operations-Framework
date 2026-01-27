import json
import os
import time

CACHE_FILE = "data/cache/threat_intel_cache.json"
CACHE_TTL = 86400  # 24 hours

os.makedirs("data/cache", exist_ok=True)

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_cached_ioc(ioc):
    cache = load_cache()
    if ioc in cache:
        if time.time() - cache[ioc]["timestamp"] < CACHE_TTL:
            return cache[ioc]["data"]
    return None

def cache_ioc(ioc, data):
    cache = load_cache()
    cache[ioc] = {
        "timestamp": time.time(),
        "data": data
    }
    save_cache(cache)
