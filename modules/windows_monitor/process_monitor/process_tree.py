import psutil
import os

def get_process_tree():
    processes = []

    for proc in psutil.process_iter(attrs=["pid", "ppid", "name", "exe"]):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            continue

    return processes


def detect_suspicious_parent_child():
    alerts = []
    tree = get_process_tree()

    for proc in tree:
        parent = next((p for p in tree if p["pid"] == proc["ppid"]), None)
        if not parent:
            continue

        # Simple suspicious rule
        if parent["name"].lower() in ["winword.exe", "excel.exe"] \
           and proc["name"].lower() in ["cmd.exe", "powershell.exe"]:
            alerts.append({
                "parent": parent["name"],
                "child": proc["name"],
                "pid": proc["pid"]
            })

    return alerts
