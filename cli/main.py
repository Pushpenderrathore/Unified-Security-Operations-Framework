import argparse
from modules.usb_monitor.device_events import monitor_usb
from modules.pdf_malware.static_scan import scan_pdf
from modules.pdf_malware.indicators import generate_verdict
from modules.threat_intel.feeds import check_ip_reputation
from modules.threat_intel.cache import get_cached_ioc, cache_ioc
from modules.threat_intel.risk_score import calculate_risk


def main():
    parser = argparse.ArgumentParser(description="Unified SOC Framework")

    parser.add_argument(
        "--module",
        choices=["usb_monitor", "pdf_malware", "threat_intel"],
        required=True,
        help="Module to run"
    )

    parser.add_argument(
        "--file",
        help="File path or IOC (used by pdf_malware and threat_intel modules)"
    )

    args = parser.parse_args()

    # USB MONITOR
    if args.module == "usb_monitor":
        monitor_usb()

    # PDF MALWARE ANALYSIS
    elif args.module == "pdf_malware":
        if not args.file:
            print("[!] Error: --file argument is required for pdf_malware")
            return

        findings = scan_pdf(args.file)
        verdict = generate_verdict(findings)

        print("\n--- PDF Malware Scan Result ---")
        print("Findings:", findings)
        print("Verdict:", verdict)

    # THREAT INTELLIGENCE
    elif args.module == "threat_intel":
        if not args.file:
            print("[!] Error: Provide IOC (IP/domain) using --file")
            return

        cached = get_cached_ioc(args.file)
        if cached:
            data = cached
            print("[+] Using cached result")
        else:
            data = check_ip_reputation(args.file)
            cache_ioc(args.file, data)

        risk = calculate_risk(data)

        print("\n--- Threat Intelligence Report ---")
        print("IOC:", args.file)
        print("Abuse Confidence:", data["data"]["abuseConfidenceScore"])
        print("Risk Level:", risk)


if __name__ == "__main__":
    main()
