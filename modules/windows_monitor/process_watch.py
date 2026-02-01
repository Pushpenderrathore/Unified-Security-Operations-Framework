import os
import psutil
import time
import hashlib

if os.name != "nt":
    raise RuntimeError("Windows only")

KNOWN = set()


def hash_exe(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    except Exception:
        return None


def watch_processes(interval=3):
    alerts = []

    while True:
        for p in psutil.process_iter(attrs=["pid", "name", "exe", "ppid"]):
            try:
                pid = p.info["pid"]
                if pid not in KNOWN:
                    KNOWN.add(pid)
                    exe = p.info.get("exe")
                    h = hash_exe(exe) if exe else None

                    alerts.append({
                        "pid": pid,
                        "name": p.info["name"],
                        "exe": exe,
                        "hash": h,
                        "ppid": p.info["ppid"]
                    })
            except Exception:
                pass

        time.sleep(interval)

