import csv, os
from collections import deque
from flask import Flask, render_template

DATA = "/data/readings.csv"

app = Flask(__name__)

def latest_by_node():
    if not os.path.exists(DATA):
        return []
    with open(DATA, newline="") as f:
        rows = deque(csv.DictReader(f), maxlen=200)
    latest = {}
    for r in rows:
        latest[r["node"]] = r
    nodes = []
    for node, r in sorted(latest.items()):
        try:
            nodes.append({"node": node,
                          "temp_f": f"{float(r['temp_f']):.1f}",
                          "humidity": f"{float(r['humidity']):.0f}",
                          "light_lvl": f"{float(r['light_lvl']):.0f}"
                          })
        except (ValueError, TypeError, KeyError):
            continue
    return nodes

@app.route("/")
def index():
    return render_template("index.html", nodes=latest_by_node())
