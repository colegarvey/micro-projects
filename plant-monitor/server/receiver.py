import csv, hmac, json, os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

API_KEY = os.environ["API_KEY"]
FILE = os.path.expanduser("~/plant-monitor/readings.csv")
FIELDS = ["timestamp", "node", "temp_f", "humidity", "light_lvl"]

os.makedirs(os.path.dirname(FILE), exist_ok=True)

if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
    with open(FILE, "w", newline="") as f: csv.writer(f).writerow(FIELDS)

class Handler(BaseHTTPRequestHandler):
    def reply(self, code, text=""):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(text.encode())

    def do_POST(self):

        if self.path != "/reading":
            return self.reply(404)

        key = self.headers.get("X-Api-Key", "")

        if not hmac.compare_digest(key, API_KEY):
            return self.reply(401, "denied")

        length = int(self.headers.get("Content-Length", 0))

        if length <= 0 or length > 1024:
            return self.reply(400, "bad size")

        try:
            d = json.loads(self.rfile.read(length))

            row = [
                datetime.now().isoformat(timespec="seconds"),
                str(d["node"])[:32],
                float(d["temp_f"]),
                float(d["humidity"]),
                float(d["light_lvl"])
            ]

        except (ValueError, KeyError, TypeError):
            return self.reply(400, "bad data")

        with open(FILE, "a", newline="") as f:
            csv.writer(f).writerow(row)
            f.flush()
            os.fsync(f.fileno())

        self.reply(200, "ok")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
