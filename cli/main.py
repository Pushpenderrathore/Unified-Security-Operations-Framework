import argparse
import json
import os

from modules.usb_monitor.device_events import monitor_usb
from modules.pdf_malware.static_scan import scan_pdf
from modules.pdf_malware.indicators import generate_verdict

from modules.threat_intel.feeds import check_ip_reputation
from modules.threat_intel.cache import get_cached_ioc, cache_ioc
from modules.threat_intel.risk_score import calculate_risk
from modules.threat_intel.report import generate_report as ti_generate_report

from modules.linux_privesc.enumerator import get_system_info
from modules.linux_privesc.exploit_mapper import classify_suid_binaries
from modules.linux_privesc.misconfig import (
    find_suid_binaries,
    check_sudo_permissions,
    find_writable_cron
)
from modules.linux_privesc.report import generate_report as privesc_generate_report


def save_output(report, path):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[+] Report saved to {path}")


def main():
    parser = argparse.ArgumentParser(description="Unified SOC Framework")

    parser.add_argument(
        "--module",
        choices=[
            "linux_privesc",
            "threat_intel",
            "pdf_malware",
            "usb_monitor",
            "file_transfer",
            "windows_process",
            "windows_registry",
            "web_ids"
        ],
        required=True,
        help="Module to run"
    )

    parser.add_argument(
        "--file",
        help="Input file (PDF / IOC / log / request dump)"
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

    # =========================
    # USB MONITOR
    # =========================
    if args.module == "usb_monitor":
        events = monitor_usb(verbose=args.verbose)

        if args.output and events is not None:
            save_output(events, args.output)

    # =========================
    # PDF MALWARE ANALYSIS
    # =========================
    elif args.module == "pdf_malware":
        if not args.file:
            print("[!] Error: --file argument is required for pdf_malware")
            return

        try:
            findings = scan_pdf(args.file)
        except FileNotFoundError:
            print(f"[!] PDF file not found: {args.file}")
            return
        except Exception as e:
            print(f"[!] PDF scan failed: {e}")
            return

        verdict = generate_verdict(findings)

        report = {
            "file": args.file,
            "findings": findings,
            "verdict": verdict
        }

        print("\n--- PDF Malware Scan Result ---")
        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)


    # =========================
    # FILE TRANSFER MONITOR
    # =========================
    elif args.module == "file_transfer":
        from modules.file_transfer_monitor.watcher import start
        from modules.file_transfer_monitor.report import generate_report

        print("[*] Monitoring file transfers (CTRL+C to stop)...")

        try:
            events = start("/tmp")
        except KeyboardInterrupt:
            print("\n[*] Stopping monitor...")

        report = generate_report(events)
        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)

    # =========================
    # WEB IDS
    # =========================
    elif args.module == "web_ids":
        from modules.web_ids.rules import detect_attack

        payload = ""
        if args.file:
            with open(args.file, "r", errors="ignore") as f:
                payload = f.read()

        alerts = detect_attack(payload)
        report = {
            "alerts": alerts,
            "total_alerts": len(alerts)
        }

        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)

    # =========================
    # WINDOWS PROCESS MONITOR
    # =========================
    elif args.module == "windows_process":
        if os.name != "nt":
            print("[!] windows_process module can run only on Windows")
            return

        from modules.windows_monitor.process_monitor.process_tree import (
            detect_suspicious_parent_child
        )

        alerts = detect_suspicious_parent_child()
        report = {
            "suspicious_process_chains": alerts,
            "count": len(alerts)
        }

        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)

    # =========================
    # WINDOWS REGISTRY MONITOR
    # =========================
    elif args.module == "windows_registry":
        if os.name != "nt":
            print("[!] windows_registry module can run only on Windows")
            return

        from modules.windows_monitor.registry_monitor.monitor import monitor_registry

        report = monitor_registry()
        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)

    # =========================
    # THREAT INTELLIGENCE
    # =========================
    elif args.module == "threat_intel":
        if not args.file:
            print("[!] Error: Provide IOC using --file")
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
        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)

    # =========================
    # LINUX PRIVILEGE ESCALATION
    # =========================
    elif args.module == "linux_privesc":
        system = get_system_info()

        if system["uid"] == 0:
            print("[!] Running as root: checks reflect persistence risk")

        suid_list = find_suid_binaries()
        suid_analysis = classify_suid_binaries(suid_list)
        sudo_rules = check_sudo_permissions()
        cron = find_writable_cron()

        report = privesc_generate_report(
            system,
            suid_analysis,
            sudo_rules,
            cron
        )

        print("\n--- Linux Privilege Escalation Report ---")
        print(json.dumps(report, indent=2))

        if args.output:
            save_output(report, args.output)


if __name__ == "__main__":
    main()
