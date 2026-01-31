import os
import subprocess
from core.logger import get_logger

logger = get_logger("linux_privesc")

def find_suid_binaries():
    result = subprocess.run(
        ["find", "/", "-perm", "-4000", "-type", "f"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False
    )

    return [line for line in result.stdout.split("\n") if line.strip()]

def check_sudo_permissions():
    try:
        output = subprocess.check_output(["sudo", "-l"], stderr=subprocess.DEVNULL, text=True)
        return output if "NOPASSWD" in output else None
    except Exception:
        return None

def find_writable_cron():
    cron_paths = ["/etc/crontab", "/etc/cron.d"]
    return [p for p in cron_paths if os.access(p, os.W_OK)]
