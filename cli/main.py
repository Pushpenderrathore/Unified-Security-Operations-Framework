import argparse
import json
from modules.usb_monitor.device_events import monitor_usb
from modules.pdf_malware.static_scan import scan_pdf
from modules.pdf_malware.indicators import generate_verdict
from modules.threat_intel.feeds import check_ip_reputation
from modules.threat_intel.cache import get_cached_ioc, cache_ioc
from modules.threat_intel.risk_score import calculate_risk
from modules.threat_intel.report import generate_report as ti_generate_report
from modules.linux_privesc.enumerator import get_system_info
from modules.linux_privesc.misconfig import (
    find_suid_binaries,
    check_sudo_permissions,
    find_writable_cron
)
from modules.linux_privesc.report import generate_report as privesc_generate_report

def main():
    parser = argparse.ArgumentParser(description="Unified SOC Framework")

    parser.add_argument(
        "--module",
        choices=["usb_monitor", "pdf_malware", "threat_intel", "linux_privesc"],
        required=True,
        help="Module to run"
    )

    parser.add_argument(
        "--file",
        help="Input target (PDF file path for pdf_malware | IP/Domain for threat_intel)"
    )

    parser.add_argument(
        "--output",
        help="Save report to file (JSON format)"
    )   

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )


    args = parser.parse_args()
    if args.verbose:
        print("[*] Verbose mode enabled")


    # USB MONITOR
    if args.module == "usb_monitor":
        monitor_usb(verbose=args.verbose)

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
            if not data:
                print("[!] Threat intel lookup failed")
                return
            cache_ioc(args.file, data)
    
        risk = calculate_risk(data)
        report = ti_generate_report(args.file, data, risk)
    
        print("\n--- Threat Intelligence Report ---")
        for k, v in report.items():
            print(f"{k}: {v}")
    
        if args.output:
            with open(args.output, "w") as f:
                json.dump(report, f, indent=2)
            print(f"[+] Report saved to {args.output}")


    # LINUX PRIVESC
    elif args.module == "linux_privesc":
        system = get_system_info()
        suid = find_suid_binaries()
        sudo_rules = check_sudo_permissions()
        cron = find_writable_cron()

        report = privesc_generate_report(system, suid, sudo_rules, cron)

        print("\n--- Linux Privilege Escalation Report ---")
        for k, v in report.items():
            print(f"{k}: {v}")
        
        if args.output:
            with open(args.output, "w") as f:
                json.dump(report, f, indent=2)
            print(f"[+] Report saved to {args.output}")

if __name__ == "__main__":
    main()
