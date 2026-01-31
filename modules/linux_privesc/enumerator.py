import os
import subprocess
from core.logger import get_logger

logger = get_logger("linux_privesc")

def get_system_info():
    info = {}
    info["user"] = os.getlogin()
    info["uid"] = os.getuid()

    try:
        info["kernel"] = subprocess.check_output(["uname", "-r"], text=True).strip()
        info["os"] = subprocess.check_output(["lsb_release", "-d"], text=True).strip()
    except Exception:
        info["os"] = "Unknown"

    return info
