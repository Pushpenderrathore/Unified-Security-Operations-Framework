import subprocess
from core.logger import get_logger

logger = get_logger("usb_monitor")

def monitor_usb():
    logger.info("Starting USB device monitoring")

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

    except KeyboardInterrupt:
        logger.info("USB monitoring stopped by user")

    finally:
        process.terminate()
        logger.info("USB monitor process terminated cleanly")
        print("\n[+] USB monitoring stopped safely")
