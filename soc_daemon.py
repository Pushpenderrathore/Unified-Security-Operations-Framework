import time
import threading
import logging

from modules.web_ids.engine import inspect
from modules.file_transfer_monitor.watcher import start as file_watch
from modules.linux_privesc.enumerator import get_system_info
from modules.linux_privesc.misconfig import find_suid_binaries
from modules.linux_privesc.exploit_mapper import classify_suid_binaries

logging.basicConfig(
    filename="data/logs/soc_daemon.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def web_ids_loop():
    logging.info("Web IDS daemon started")
    while True:
        # Example simulated input (replace with log ingestion later)
        inspect("127.0.0.1", "<script>alert(1)</script>")
        time.sleep(10)

def file_monitor_loop():
    logging.info("File transfer monitor started")
    file_watch("/tmp")

def privesc_check_loop():
    logging.info("Privilege escalation monitor started")
    while True:
        system = get_system_info()
        suid = find_suid_binaries()
        classify_suid_binaries(suid)
        time.sleep(3600)  # every 1 hour

def main():
    threads = []

    t1 = threading.Thread(target=web_ids_loop, daemon=True)
    t2 = threading.Thread(target=file_monitor_loop, daemon=True)
    t3 = threading.Thread(target=privesc_check_loop, daemon=True)

    threads.extend([t1, t2, t3])

    for t in threads:
        t.start()

    logging.info("Unified SOC Daemon running")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
