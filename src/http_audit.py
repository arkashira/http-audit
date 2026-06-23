import argparse
import json
from dataclasses import dataclass
from enum import Enum
from typing import List

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

@dataclass
class HTTPRequest:
    method: HTTPMethod
    url: str
    headers: dict
    body: str

@dataclass
class HTTPResponse:
    status_code: int
    headers: dict
    body: str

class HTTPAudit:
    def __init__(self):
        self.traffic = []

    def capture(self, request: HTTPRequest, response: HTTPResponse):
        self.traffic.append((request, response))

    def filter(self, method: HTTPMethod = None, url: str = None):
        filtered_traffic = []
        for request, response in self.traffic:
            if (method is None or request.method == method) and (url is None or request.url == url):
                filtered_traffic.append((request, response))
        return filtered_traffic

    def export(self, traffic):
        data = []
        for request, response in traffic:
            data.append({
                "method": request.method.value,
                "url": request.url,
                "headers": request.headers,
                "body": request.body,
                "status_code": response.status_code,
                "response_headers": response.headers,
                "response_body": response.body
            })
        return json.dumps(data, indent=4)

def main():
    parser = argparse.ArgumentParser(description="HTTP Audit Tool")
    parser.add_argument("--filter-method", help="Filter by HTTP method")
    parser.add_argument("--filter-url", help="Filter by URL")
    parser.add_argument("--export", action="store_true", help="Export HTTP traffic data")
    args = parser.parse_args()

    audit = HTTPAudit()
    # Simulate capturing HTTP traffic
    audit.capture(HTTPRequest(HTTPMethod.GET, "https://example.com", {"Accept": "application/json"}, ""), HTTPResponse(200, {"Content-Type": "application/json"}, "{\"message\": \"Hello World\"}"))
    audit.capture(HTTPRequest(HTTPMethod.POST, "https://example.com", {"Content-Type": "application/json"}, "{\"name\": \"John Doe\"}"), HTTPResponse(201, {"Location": "/users/1"}, "{\"id\": 1, \"name\": \"John Doe\"}"))

    if args.filter_method:
        method = HTTPMethod(args.filter_method)
    else:
        method = None

    if args.filter_url:
        url = args.filter_url
    else:
        url = None

    filtered_traffic = audit.filter(method, url)

    if args.export:
        print(audit.export(filtered_traffic))
    else:
        for request, response in filtered_traffic:
            print(f"Method: {request.method.value}, URL: {request.url}, Status Code: {response.status_code}")

if __name__ == "__main__":
    main()
