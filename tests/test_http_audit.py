import pytest
from http_audit import HTTPAudit, HTTPRequest, HTTPResponse, HTTPMethod

def test_capture():
    audit = HTTPAudit()
    request = HTTPRequest(HTTPMethod.GET, "https://example.com", {"Accept": "application/json"}, "")
    response = HTTPResponse(200, {"Content-Type": "application/json"}, "{\"message\": \"Hello World\"}")
    audit.capture(request, response)
    assert len(audit.traffic) == 1

def test_filter_method():
    audit = HTTPAudit()
    request1 = HTTPRequest(HTTPMethod.GET, "https://example.com", {"Accept": "application/json"}, "")
    response1 = HTTPResponse(200, {"Content-Type": "application/json"}, "{\"message\": \"Hello World\"}")
    request2 = HTTPRequest(HTTPMethod.POST, "https://example.com", {"Content-Type": "application/json"}, "{\"name\": \"John Doe\"}")
    response2 = HTTPResponse(201, {"Location": "/users/1"}, "{\"id\": 1, \"name\": \"John Doe\"}")
    audit.capture(request1, response1)
    audit.capture(request2, response2)
    filtered_traffic = audit.filter(HTTPMethod.GET)
    assert len(filtered_traffic) == 1
    assert filtered_traffic[0][0].method == HTTPMethod.GET

def test_filter_url():
    audit = HTTPAudit()
    request1 = HTTPRequest(HTTPMethod.GET, "https://example.com", {"Accept": "application/json"}, "")
    response1 = HTTPResponse(200, {"Content-Type": "application/json"}, "{\"message\": \"Hello World\"}")
    request2 = HTTPRequest(HTTPMethod.GET, "https://example.org", {"Accept": "application/json"}, "")
    response2 = HTTPResponse(200, {"Content-Type": "application/json"}, "{\"message\": \"Hello World\"}")
    audit.capture(request1, response1)
    audit.capture(request2, response2)
    filtered_traffic = audit.filter(url="https://example.com")
    assert len(filtered_traffic) == 1
    assert filtered_traffic[0][0].url == "https://example.com"

def test_export():
    audit = HTTPAudit()
    request = HTTPRequest(HTTPMethod.GET, "https://example.com", {"Accept": "application/json"}, "")
    response = HTTPResponse(200, {"Content-Type": "application/json"}, "{\"message\": \"Hello World\"}")
    audit.capture(request, response)
    exported_data = audit.export(audit.traffic)
    assert exported_data.startswith("[")
    assert exported_data.endswith("]")
