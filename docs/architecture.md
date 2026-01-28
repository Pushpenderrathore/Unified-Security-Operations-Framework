# Unified SOC Framework – Architecture

## Overview
The Unified SOC Framework is a modular, detection-focused security tool designed to simulate
core Security Operations Center (SOC) capabilities in an ethical and defensive manner.

The framework follows a **central CLI + modular engine architecture**, allowing each security
capability to operate independently while sharing common utilities such as logging and configuration.

---

## High-Level Architecture   
    
CLI (run.py / main.py)            
         |    
         v    
+----------------------+   
| Core Dispatcher      |   
| (Argument Parsing)   |   
+----------------------+     
         |   
         v   
+----------------------+   
| Security Modules     |    
+----------------------+    
---   

## Core Components

### 1. CLI Layer
- Handles user input (`--module`, `--file`, `--output`)
- Dispatches execution to the selected module
- Ensures clean separation between modules

### 2. Core Utilities
- Centralized logging
- Secure configuration handling (environment variables)
- Shared helpers

---

## Security Modules

### USB Monitor
- Detects USB insert/remove events
- Logs device metadata
- Continuous monitoring with graceful shutdown

### PDF Malware Analyzer
- Static analysis only
- Detects suspicious indicators (JavaScript, embedded objects)
- No execution or sandboxing

### Threat Intelligence Module
- Enriches IOCs using AbuseIPDB
- Uses caching to reduce API usage
- Produces structured SOC-style reports

### Linux Privilege Escalation Analyzer
- Detects misconfigurations (SUID, sudo rules, cron permissions)
- No exploitation performed
- Risk-focused reporting

---

## Design Principles
- Modular & extensible
- Detection-first approach
- Ethical security research
- Production-style reporting
- Secure secret management

---

## Future Extensions
- Web dashboard
- SIEM integration
- Additional threat intelligence feeds
- Windows host monitoring expansion
