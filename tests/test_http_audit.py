import pytest
from src.http_audit import HttpAudit, HttpEvent

def test_http_audit_run():
    http_audit = HttpAudit(True, "https://example.com", {"alert": "true"})
    http_events = http_audit.run()
    assert len(http_events) == 1
    assert http_events[0].url == "https://example.com"
    assert http_events[0].method == "GET"
    assert http_events[0].status == 200

def test_http_audit_report():
    http_audit = HttpAudit(True, "https://example.com", {"alert": "true"})
    http_events = http_audit.run()
    reported_events = http_audit.report()
    assert reported_events == http_events

def test_http_audit_e_bpf_capability_false():
    http_audit = HttpAudit(False, "https://example.com", {"alert": "true"})
    http_events = http_audit.run()
    assert len(http_events) == 1
    assert http_events[0].url == "https://example.com"
    assert http_events[0].method == "GET"
    assert http_events[0].status == 200

def test_http_audit_remote_endpoint_empty():
    http_audit = HttpAudit(True, "", {"alert": "true"})
    http_events = http_audit.run()
    assert len(http_events) == 1
    assert http_events[0].url == "https://example.com"
    assert http_events[0].method == "GET"
    assert http_events[0].status == 200

def test_http_audit_alert_config_empty():
    http_audit = HttpAudit(True, "https://example.com", {})
    http_events = http_audit.run()
    assert len(http_events) == 1
    assert http_events[0].url == "https://example.com"
    assert http_events[0].method == "GET"
    assert http_events[0].status == 200
