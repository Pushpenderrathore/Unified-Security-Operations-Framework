from modules.core_shared.unified_report import unify

def test_unified():
    r = unify({"a": {"ok": True}})
    assert "modules" in r

