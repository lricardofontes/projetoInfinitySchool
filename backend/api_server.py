import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from backend.controllers.user_controller import (
    create_user_handler, get_user_handler,
    update_user_handler, delete_user_handler,
    login_handler
)
from backend.controllers.resource_controller import (
    create_resource_handler, list_resources_handler,
    get_resource_handler, update_resource_handler,
    delete_resource_handler
)

HOST, PORT = "0.0.0.0", 8000

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        # apenas devolve cabeçalhos CORS
        self._set_headers(HTTPStatus.OK)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        path = urlparse(self.path).path

        # defaults
        status, response = HTTPStatus.NOT_FOUND, {"error": "Not found"}

        if path == "/users":
            status, response = create_user_handler(body)
        elif path == "/login":
            status, response = login_handler(body)
        elif path == "/resources":
            status, response = create_resource_handler(body)

        self._set_headers(status)
        if response is not None:
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")

        status, response = HTTPStatus.NOT_FOUND, {"error": "Not found"}

        # /resources
        if path == "/resources":
            status, response = list_resources_handler()
        # /resources/:id
        elif len(parts) == 2 and parts[0] == "resources" and parts[1].isdigit():
            status, response = get_resource_handler(int(parts[1]))
        # /users/:id
        elif len(parts) == 2 and parts[0] == "users" and parts[1].isdigit():
            status, response = get_user_handler(int(parts[1]))

        self._set_headers(status)
        if response is not None:
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_PUT(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        parts = self.path.strip("/").split("/")

        status, response = HTTPStatus.NOT_FOUND, {"error": "Not found"}

        # PUT /users/:id
        if len(parts) == 2 and parts[0] == "users" and parts[1].isdigit():
            status, response = update_user_handler(int(parts[1]), body)
        # PUT /resources/:id
        elif len(parts) == 2 and parts[0] == "resources" and parts[1].isdigit():
            status, response = update_resource_handler(int(parts[1]), body)

        self._set_headers(status)
        if response is not None:
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_DELETE(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")

        status, response = HTTPStatus.NOT_FOUND, {"error": "Not found"}

        # DELETE /users/:id
        if len(parts) == 2 and parts[0] == "users" and parts[1].isdigit():
            status, response = delete_user_handler(int(parts[1]))
        # DELETE /resources/:id
        elif len(parts) == 2 and parts[0] == "resources" and parts[1].isdigit():
            status, response = delete_resource_handler(int(parts[1]))

        self._set_headers(status)
        if response is not None:
            self.wfile.write(json.dumps(response).encode("utf-8"))

def run():
    httpd = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()