import subprocess
import csv
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
    ping = round(data['ping']['latency'], 2)
    download = round(data['download']['bandwidth'] / 125000, 2)  # Convert to Mbps
    upload = round(data['upload']['bandwidth'] / 125000, 2)      # Convert to Mbps
    isp = data['isp']
    server = data['server']['name']

    # Prepare formatted strings
    formatted_output = [
        f"📅 Date & Time: {timestamp}",
        f"📡 Ping: {ping} ms",
        f"⬇️ Download Speed: {download} Mbps",
        f"⬆️ Upload Speed: {upload} Mbps",
        f"🏢 ISP: {isp}",
        f"🌐 Server: {server}",
    ]

    # Save to CSV as one cell per line
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["📊 Network Speed Test Result"])
        for line in formatted_output:
            writer.writerow([line])
        writer.writerow([])  # Add a blank line between entries

    # Print formatted output
    print("\n📊 Network Speed Test Result")
    for line in formatted_output:
        print(line)
    print()

def main():
    print("[*] Running network speed test...")
    json_result = run_speedtest()
    if json_result:
        parse_and_log(json_result)

if __name__ == '__main__':
    main()
