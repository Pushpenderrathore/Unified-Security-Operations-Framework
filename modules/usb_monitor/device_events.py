import subprocess
from core.logger import get_logger

logger = get_logger("usb_monitor")

def monitor_usb(verbose=False):
    logger.info("Starting USB device monitoring")

    if verbose:
        print("[VERBOSE] USB monitoring started")
    
    cmd = ["udevadm", "monitor", "--subsystem-match=usb", "--property"]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in process.stdout:
            if "ID_VENDOR_ID" in line or "ID_MODEL_ID" in line:
                logger.info(line.strip())
                if verbose:
                    print(f"[VERBOSE] {line.strip()}")

    except KeyboardInterrupt:
        logger.info("USB monitoring stopped by user")

    finally:
        process.terminate()
        logger.info("USB monitor process terminated cleanly")
        print("\n[+] USB monitoring stopped safely")
