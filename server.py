from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

# Directory where the script runs (Render will use this as working dir)
ROOT_DIR = os.getcwd()

# Absolute fallback path (e.g. mock_campaign.json)
FALLBACK_FILE = os.path.join(ROOT_DIR, "mock_campaign.json")

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Sanitize path
        safe_path = self.path.strip("/").replace("/", os.sep)
        requested_path = os.path.normpath(os.path.join(ROOT_DIR, safe_path))

        print(f"Requested URL: {self.path}")
        print(f"Resolved to: {requested_path}")

        if os.path.isfile(requested_path):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            with open(requested_path, "rb") as f:
                self.wfile.write(f.read())
        elif os.path.isfile(FALLBACK_FILE):
            print("Requested file not found. Serving fallback: mock_campaign.json.")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            with open(FALLBACK_FILE, "rb") as f:
                self.wfile.write(f.read())
        else:
            print("File not found, and fallback also missing.")
            self.send_error(404, "File not found.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render assigns dynamic ports
    httpd = HTTPServer(('0.0.0.0', port), CustomHandler)
    print(f"Server running on http://0.0.0.0:{port}")
    httpd.serve_forever()
