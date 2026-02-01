def log_usb_event(device_id, action):
    return {
        "device_id": device_id,
        "action": action,
        "status": "BLOCKED" if action == "unauthorized" else "ALLOWED"
    }
