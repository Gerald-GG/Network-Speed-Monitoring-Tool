from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import subprocess
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Load last 10 entries from raw_data.csv
    data = []
    try:
        df = pd.read_csv('logs/raw_data.csv')
        last_entries = df.tail(10).iloc[::-1]  # Reverse to show newest first
        data = last_entries.to_dict(orient='records')
    except Exception as e:
        print(f"[!] Could not read raw_data.csv: {e}")

    return render_template('index.html', data=data)

@app.route('/graph')
def graph():
    return send_from_directory('logs', 'speed_graph.png')

@app.route('/run-scan')
def run_scan():
    try:
        subprocess.run(['python3', 'speedtest_monitor.py', '--run'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during scan: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
