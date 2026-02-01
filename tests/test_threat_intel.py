from modules.threat_intel.correlator import correlate

def test_correlation():
    data = [
        {"malicious": True, "score": 80},
        {"malicious": False, "score": 0}
    ]
    r = correlate(data)
    assert r["sources_flagged"] == 1

