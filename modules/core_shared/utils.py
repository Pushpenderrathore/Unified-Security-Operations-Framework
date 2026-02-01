import os

def require_windows():
    if os.name != "nt":
        raise RuntimeError("Windows-only module")

def require_linux():
    if os.name != "posix":
        raise RuntimeError("Linux-only module")
