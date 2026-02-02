from modules.usb_monitor.audit import log_event

def test_usb_log():
    e = log_event("USB123", False)
    assert e["status"] == "BLOCKED"

