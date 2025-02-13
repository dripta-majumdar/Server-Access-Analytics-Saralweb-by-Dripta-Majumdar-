# from flask import Flask, jsonify
# import re
# from collections import defaultdict

# app = Flask(__name__)

# # Regular expression to capture IP, day, and hour from a log line.
# pattern = re.compile(
#     r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<day>\d+\/[A-Za-z]+\/\d+):(?P<hour>\d+):\d+:\d+'
# )

# # Path to the log file
# log_file = "c:/Users/LENOVO/OneDrive/Desktop/SaralWeb Assignment/log.txt"

# # Dictionaries to store counts for IP addresses and hourly hits.
# ip_counts = defaultdict(int)
# hour_counts = defaultdict(int)
# total_hits = 0

# # Choose the day to analyze (e.g., "30/Jan/2024")
# target_day = "30/Jan/2024"

# # Read and parse the log file.
# def parse_log():
#     global ip_counts, hour_counts, total_hits
#     try:
#         with open(log_file, 'r') as f:
#             for line in f:
#                 match = pattern.search(line)
#                 if match:
#                     day = match.group('day')
#                     if day == target_day:
#                         ip = match.group('ip')
#                         hour = match.group('hour')
#                         ip_counts[ip] += 1
#                         hour_counts[hour] += 1
#                         total_hits += 1
#     except FileNotFoundError:
#         print(f"Error: The file {log_file} was not found.")
#         exit(1)

# # Calculate contributors
# def calculate_contributors(data, threshold_percent):
#     sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
#     accumulated = 0
#     threshold = (threshold_percent / 100) * total_hits
#     contributors = []

#     for key, count in sorted_items:
#         contributors.append([key, count])
#         accumulated += count
#         if accumulated >= threshold:
#             break
#     return contributors

# # API endpoint to serve data
# @app.route('/api/data', methods=['GET'])
# def get_data():
#     parse_log()
#     data = {
#         "ip_histogram": dict(ip_counts),
#         "hour_histogram": dict(hour_counts),
#         "top_ips": calculate_contributors(ip_counts, 85),
#         "top_hours": calculate_contributors(hour_counts, 70)
#     }
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)





# from flask import Flask, jsonify
# from flask_cors import CORS
# import re
# from collections import defaultdict

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Regular expression to capture IP, day, and hour from a log line.
# pattern = re.compile(
#     r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<day>\d+\/[A-Za-z]+\/\d+):(?P<hour>\d+):\d+:\d+'
# )

# # Path to the log file
# log_file = "c:/Users/LENOVO/OneDrive/Desktop/SaralWeb Assignment/Backend/log.txt"

# # Dictionaries to store counts for IP addresses and hourly hits.
# ip_counts = defaultdict(int)
# hour_counts = defaultdict(int)
# total_hits = 0

# # Choose the day to analyze (e.g., "30/Jan/2024")
# target_day = "30/Jan/2024"

# # Read and parse the log file.
# def parse_log():
#     global ip_counts, hour_counts, total_hits
#     try:
#         with open(log_file, 'r') as f:
#             for line in f:
#                 match = pattern.search(line)
#                 if match:
#                     day = match.group('day')
#                     if day == target_day:
#                         ip = match.group('ip')
#                         hour = match.group('hour')
#                         ip_counts[ip] += 1
#                         hour_counts[hour] += 1
#                         total_hits += 1
#     except FileNotFoundError:
#         print(f"Error: The file {log_file} was not found.")
#         exit(1)

# # Calculate contributors
# def calculate_contributors(data, threshold_percent):
#     sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
#     accumulated = 0
#     threshold = (threshold_percent / 100) * total_hits
#     contributors = []

#     for key, count in sorted_items:
#         contributors.append([key, count])
#         accumulated += count
#         if accumulated >= threshold:
#             break
#     return contributors

# # Root route for the homepage
# @app.route('/')
# def home():
#     return "Welcome to the Log Parser Dashboard! Visit /api/data for analytics."

# # API endpoint for data
# @app.route('/api/data')
# def get_data():
#     parse_log()  # Parse the log file and populate ip_counts, hour_counts, etc.
#     data = {
#         "ip_histogram": dict(ip_counts),
#         "hour_histogram": dict(hour_counts),
#         "top_ips": calculate_contributors(ip_counts, 85),
#         "top_hours": calculate_contributors(hour_counts, 70)
#     }
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import re
import os
from collections import defaultdict
import logging

app = Flask(__name__, static_folder='build', static_url_path='/')
CORS(app)
app.logger.setLevel(logging.DEBUG)

LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?\[(?P<day>\d{2}/[A-Za-z]+/\d{4}):(?P<hour>\d{2}):\d{2}:\d{2}'
)
LOG_FILE = r"C:\Users\LENOVO\OneDrive\Desktop\SaralWeb Assignment\Backend\log.txt"
TARGET_DAY = "30/Jan/2024"

def parse_log():
    ip_counts = defaultdict(int)
    hour_counts = defaultdict(int)
    total_hits = 0
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if match := LOG_PATTERN.search(line):
                    if match.group('day') == TARGET_DAY:
                        ip = match.group('ip')
                        hour = match.group('hour')
                        ip_counts[ip] += 1
                        hour_counts[hour] += 1
                        total_hits += 1
    except Exception as e:
        app.logger.error(f"Failed to parse log file: {str(e)}")
        raise RuntimeError("Error processing log file")
    
    return ip_counts, hour_counts, total_hits

def calculate_contributors(data, total, threshold_percent):
    sorted_items = sorted(data.items(), key=lambda x: -x[1])
    threshold = (threshold_percent / 100) * total
    accumulated = 0
    contributors = []
    
    for key, count in sorted_items:
        contributors.append([key, count])
        accumulated += count
        if accumulated >= threshold:
            break
    return contributors

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/data')
def get_data():
    try:
        ip_counts, hour_counts, total = parse_log()

        ip_histogram = "IP Address           | Occurrences\n"
        ip_histogram += "-----------------------------------\n"
        for ip, count in sorted(ip_counts.items(), key=lambda x: -x[1]):
            ip_histogram += f"{ip.ljust(20)} | {count}\n"

        hourly_traffic = "Hour  | Visitors\n"
        hourly_traffic += "--------------------\n"
        for hour, count in sorted(hour_counts.items()):
            hourly_traffic += f"{hour.ljust(5)} | {count}\n"

        top_ips = "Top IPs (85% Traffic):\n"
        for ip, count in calculate_contributors(ip_counts, total, 85):
            top_ips += f"{ip}: {count} hits\n"

        top_hours = "Top Hours (70% Traffic):\n"
        for hour, count in calculate_contributors(hour_counts, total, 70):
            top_hours += f"{hour}: {count} visitors\n"

        return jsonify({
            "ip_histogram": ip_histogram,
            "hourly_traffic": hourly_traffic,
            "top_ips": top_ips,
            "top_hours": top_hours
        })
    except Exception as e:
        app.logger.error(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    app.logger.info(f"Serving index.html for unknown path: {e}")
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)