import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import main
from matomo_import import settings
from zipfile import ZipFile
# import jwt
from datetime import datetime, timedelta


class MainRequestHandler(BaseHTTPRequestHandler):  # change to meaningul name
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/zip")
        self.send_header("Content-Disposition", "attachment; filename=file.zip")
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        settings.set_env_variables()
        self._set_headers()
        zip_name = f"{os.environ['DB_NAME']}.zip"

        with ZipFile(zip_name,'w') as zip_file:
            main.exec()
            zip_file.write(os.environ['DB_NAME'])

        with open(zip_name, 'rb') as response:
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
