import os
import re
import argparse


def check_line_for_anomalies(line):
    if re.search(r"(ERROR|FATAL|TIMEOUT)", line):
        return True, "Critical Error Flag"

    latency_match = re.search(r"Latency:\s*(\d+)ms", line)
    if latency_match:
        latency_val = int(latency_match.group(1))
        if latency_val > 50:
            return True, f"High Latency ({latency_val}ms)"

    return False, None


def analyze_directory(directory_path):
    print(f"--- Analyzing logs in: {directory_path} ---\n")
    total_anomalies = 0

    if not os.path.exists(directory_path):
        print("Directory not found.")
        return

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory_path, filename)

            with open(filepath, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    is_anomaly, reason = check_line_for_anomalies(line)
                    if is_anomaly:
                        print(f"[{filename} - Line {line_num}] {reason}: {line.strip()}")
                        total_anomalies += 1

    print(f"\nScan Complete. Total anomalies found: {total_anomalies}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse hardware logs for errors and latency.")
    parser.add_argument("log_dir", help="Path to the directory containing log files")
    args = parser.parse_args()

    analyze_directory(args.log_dir)