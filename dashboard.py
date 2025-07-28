from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
