import argparse
from modules.usb_monitor.device_events import monitor_usb

def main():
    parser = argparse.ArgumentParser(description="Unified SOC Framework")
    parser.add_argument(
        "--module",
        choices=["usb_monitor"],
        required=True
    )
    args = parser.parse_args()

    if args.module == "usb_monitor":
        monitor_usb()

if __name__ == "__main__":
    main()
