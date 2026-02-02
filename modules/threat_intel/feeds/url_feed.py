import requests

def fetch(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

