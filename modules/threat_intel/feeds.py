import os
import requests
from core.logger import get_logger
# from core.config import ABUSEIPDB_API_KEY ; # API key is loaded securely from environment variables

logger = get_logger("threat_intel")

def get_api_key():
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        logger.error("ABUSEIPDB_API_KEY environment variable not set")
        raise RuntimeError("ABUSEIPDB_API_KEY is missing")
    return api_key

def check_ip_reputation(ip):
    logger.info(f"Querying AbuseIPDB for IP: {ip}")

    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={
                "Key": get_api_key(),
                "Accept": "application/json"
            },
            params={
                "ipAddress": ip,
                "maxAgeInDays": 90
            },
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Threat intel request failed: {e}")
        return None
