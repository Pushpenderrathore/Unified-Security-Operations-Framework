from modules.web_ids.engine import inspect

def test_ids():
    r = inspect("1.1.1.1", "<script>alert(1)</script>")
    assert len(r["alerts"]) > 0

