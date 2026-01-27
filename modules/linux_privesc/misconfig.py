import os
import subprocess
from core.logger import get_logger

logger = get_logger("linux_privesc")


def find_suid_binaries():
    logger.info("Searching for SUID binaries")
    try:
        result = subprocess.check_output(
            ["find", "/", "-perm", "-4000", "-type", "f"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        binaries = result.strip().split("\n")
        return binaries
    except Exception:
        return []


def check_sudo_permissions():
    """
    Checks sudo rules for dangerous NOPASSWD entries.
    This does NOT perform privilege escalation.
    """
    logger.info("Checking sudo permissions")
    try:
        output = subprocess.check_output(
            ["sudo", "-l"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        if "NOPASSWD" in output:
            return output
    except Exception:
        pass

    return None


def find_writable_cron():
    """
    Detects writable cron configuration paths.
    """
    cron_paths = ["/etc/crontab", "/etc/cron.d"]
    writable = []

    for path in cron_paths:
        try:
            if os.access(path, os.W_OK):
                writable.append(path)
        except Exception:
            pass

    return writable
