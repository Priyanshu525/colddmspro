from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

FALLBACK_FILE = os.path.join("assets", "mock_campaign.json")
ROOT_DIR = os.getcwd()

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        requested_path = os.path.normpath(os.path.join(ROOT_DIR, self.path.strip("/")))

        print(f"Requested URL: {self.path}")
        print(f"Resolved to: {requested_path}")

        if os.path.isfile(requested_path):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            with open(requested_path, 'rb') as f:
                self.wfile.write(f.read())
        elif os.path.isfile(FALLBACK_FILE):
            print("Requested file not found. Serving fallback mock_campaign.json.")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            with open(FALLBACK_FILE, 'rb') as f:
                self.wfile.write(f.read())
        else:
            print("Neither the requested file nor fallback file was found.")
            self.send_error(404, "File not found.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"Server running at http://0.0.0.0:{port}")
    httpd.serve_forever()
