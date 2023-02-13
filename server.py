import http.server
import socketserver
import os
import sys

HOSTS_FILE_PATH = "/private/etc/hosts"
API_KEY = None

class RequestHandler(http.server.BaseHTTPRequestHandler):
    # for preflight
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Max-Age", "3600")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/block"):
            query = self.path[len("/block?"):]
            parts = query.split("&")
            url = None
            key = None
            for part in parts:
                if part.startswith("url="):
                    url = part[len("url="):]
                elif part.startswith("key="):
                    key = part[len("key="):]
            if key != API_KEY:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(bytes("Unauthorized", "utf-8"))
                return
            if url is None:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes("Bad request", "utf-8"))
                return
            entry = "127.0.0.1 " + url + "\n"
            with open(HOSTS_FILE_PATH, "a") as hosts_file:
                hosts_file.write(entry)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Blocked " + url, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Not found", "utf-8"))

def main(argv):
    global API_KEY
    if len(argv) != 3:
        print("Usage: python3", argv[0], "<api-key>")
        sys.exit(1)
    API_KEY = argv[1]
    PORT = int(argv[2])
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print("Serving on port", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    main(sys.argv)