import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import main


class MainRequestHandler(BaseHTTPRequestHandler):  # change to meaningul name
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/x-sqlite3")
        self.send_header("Content-Disposition", "attachment; filename=db")
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        main.exec()
        with open(os.environ['DB_NAME'], 'rb') as response:
            self.wfile.write(response.read())


def run(
        server_class=HTTPServer,
        handler_class=MainRequestHandler,
        addr="0.0.0.0",
        port=8080
        ):
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
