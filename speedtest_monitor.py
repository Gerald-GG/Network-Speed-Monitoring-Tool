import subprocess
import csv
import datetime
import json

def run_speedtest():
    try:
        result = subprocess.run(['speedtest', '--format=json'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running speedtest: {e}")
        return None

def parse_and_log(json_data, log_file='logs/speedtest_log.csv'):
    data = json.loads(json_data)

    timestamp = data['timestamp']
    ping = data['ping']['latency']
    download = data['download']['bandwidth'] / 125000  # Convert to Mbps
    upload = data['upload']['bandwidth'] / 125000      # Convert to Mbps
    isp = data['isp']
    server = data['server']['name']

    # Log to CSV
    row = [timestamp, round(ping, 2), round(download, 2), round(upload, 2), isp, server]
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    # Print formatted result
    print("\n📊 Network Speed Test Result")
    print(f"📅 Date & Time: {timestamp}")
    print(f"📡 Ping: {round(ping, 2)} ms")
    print(f"⬇️ Download Speed: {round(download, 2)} Mbps")
    print(f"⬆️ Upload Speed: {round(upload, 2)} Mbps")
    print(f"🏢 ISP: {isp}")
    print(f"🌐 Server: {server}\n")

def main():
    print("[*] Running network speed test...")
    json_result = run_speedtest()
    if json_result:
        parse_and_log(json_result)

if __name__ == '__main__':
    main()
