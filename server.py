import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
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
        proc = subprocess.run(
            ['sqlite3', 'database', '.dump'],
            stdout=subprocess.PIPE
        )
        response = json.dumps(
            {'results': proc.stdout.decode('utf-8')}
        )
        response = bytes(response, 'utf-8')
        self.wfile.write(response)

    def _json(self, message):
        content = {'hello': message}
        return content


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
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
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
