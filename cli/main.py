import argparse
from modules.usb_monitor.device_events import monitor_usb
from modules.pdf_malware.static_scan import scan_pdf
from modules.pdf_malware.indicators import generate_verdict


def main():
    parser = argparse.ArgumentParser(description="Unified SOC Framework")

    parser.add_argument(
        "--module",
        choices=["usb_monitor", "pdf_malware"],
        required=True,
        help="Module to run"
    )

    parser.add_argument(
        "--file",
        help="PDF file path (required for pdf_malware module)"
    )

    args = parser.parse_args()

    if args.module == "usb_monitor":
        monitor_usb()

    elif args.module == "pdf_malware":
        if not args.file:
            print("[!] Error: --file argument is required for pdf_malware")
            return

        findings = scan_pdf(args.file)
        verdict = generate_verdict(findings)

        print("\n--- PDF Malware Scan Result ---")
        print("Findings:", findings)
        print("Verdict:", verdict)


if __name__ == "__main__":
    main()
