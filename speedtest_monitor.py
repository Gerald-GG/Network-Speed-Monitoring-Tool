import subprocess
import csv
import json
import argparse
import os

LOG_FILE = 'logs/speedtest_log.csv'
RAW_DATA_FILE = 'logs/raw_data.csv'

def run_speedtest():
    try:
        result = subprocess.run(['speedtest', '--format=json'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running speedtest: {e}")
        return None

def parse_and_log(json_data):
    data = json.loads(json_data)

    timestamp = data['timestamp']
    ping = round(data['ping']['latency'], 2)
    download = round(data['download']['bandwidth'] / 125000, 2)
    upload = round(data['upload']['bandwidth'] / 125000, 2)
    isp = data['isp']
    server = data['server']['name']

    # Format for display and formatted log
    formatted_output = [
        f"📅 Date & Time: {timestamp}",
        f"📡 Ping: {ping} ms",
        f"⬇️ Download Speed: {download} Mbps",
        f"⬆️ Upload Speed: {upload} Mbps",
        f"🏢 ISP: {isp}",
        f"🌐 Server: {server}",
    ]

    # Save formatted to display log
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["📊 Network Speed Test Result"])
        for line in formatted_output:
            writer.writerow([line])
        writer.writerow([])

    # Save raw values for graphing
    file_exists = os.path.isfile(RAW_DATA_FILE)
    with open(RAW_DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'ping_ms', 'download_mbps', 'upload_mbps', 'isp', 'server'])
        writer.writerow([timestamp, ping, download, upload, isp, server])

    # Print to terminal
    print("\n📊 Network Speed Test Result")
    for line in formatted_output:
        print(line)
    print()

def view_log():
    if not os.path.isfile(LOG_FILE):
        print("[!] No log file found.")
        return
    with open(LOG_FILE, 'r') as f:
        print("\n🗂️ Full Test Log:\n")
        print(f.read())

def view_last():
    if not os.path.isfile(LOG_FILE):
        print("[!] No log file found.")
        return
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        last_entry = []
        for line in reversed(lines):
            if line.strip() == "":
                break
            last_entry.insert(0, line.strip())
        print("\n📋 Last Speed Test Entry:\n")
        for line in last_entry:
            print(line)
        print()

def main():
    parser = argparse.ArgumentParser(description="Network Speed Monitoring Tool")
    parser.add_argument('--run', action='store_true', help="Run a new speed test and log results")
    parser.add_argument('--view-log', action='store_true', help="View full formatted test log")
    parser.add_argument('--last', action='store_true', help="View last test result only")
    args = parser.parse_args()

    if args.run:
        print("[*] Running network speed test...")
        json_result = run_speedtest()
        if json_result:
            parse_and_log(json_result)
    elif args.view_log:
        view_log()
    elif args.last:
        view_last()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
