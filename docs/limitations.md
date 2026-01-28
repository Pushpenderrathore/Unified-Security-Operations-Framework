# Limitations

This project is intentionally scoped for educational and defensive security purposes.

---

## General Limitations
- Not a full-scale SOC or SIEM platform
- Designed for learning and demonstration, not enterprise deployment
- No real-time alerting system (email/SMS)

---

## Module-Specific Limitations

### USB Monitor
- Monitoring only (no blocking or enforcement)
- Platform-dependent behavior

### PDF Malware Analyzer
- Static analysis only
- No dynamic execution or sandboxing
- Indicators may produce false positives

### Threat Intelligence Module
- Relies on free-tier API limits
- Limited to IP/domain reputation
- Internet connection required

### Linux PrivEsc Analyzer
- Detection-only (no exploitation)
- Results depend on system configuration
- Hardened systems may show no findings

---

## Security Boundaries
- No credential harvesting
- No payload execution
- No exploitation logic
- No persistence mechanisms

---

## Ethical Disclaimer
This project strictly adheres to ethical cybersecurity practices and is intended only
for educational and research purposes.
