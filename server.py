import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import subprocess
import os
import main


class S(BaseHTTPRequestHandler): # change to meaningul name
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        main.exec()
        data = ""
        conn = sqlite3.connect("database")
        for line in conn.iterdump():
            data += f"{line}.\n"
        response = json.dumps(
            {'results': data}
        )
        response = bytes(response, 'utf-8')
        self.wfile.write(response)


def run(server_class=HTTPServer, handler_class=S, addr="0.0.0.0", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
