def test_cli_import():
    import run
    assert hasattr(run, "main")

def test_linux_privesc_report_generation():
    from modules.linux_privesc.report import generate_report

    system = {
        "user": "test",
        "uid": 1000,
        "kernel": "test-kernel",
        "os": "test-os"
    }

    suid_analysis = {
        "total": 0,
        "dangerous": [],
        "safe": []
    }

    report = generate_report(system, suid_analysis, None, [])

    assert "summary" in report
    assert "system_info" in report
    assert report["summary"]["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
