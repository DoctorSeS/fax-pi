import os
import socket
import logging
import sys
import requests
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Function to get public IP
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        # Avoid blank lines and logger messages
        if message.rstrip() != "" and "ERROR:BotLogger" not in message:
            self.logger.log(self.log_level, message.rstrip())

    def flush(self):
        pass  # No flushing needed for logging

class IgnoreLogFilter(logging.Filter):
    def filter(self, record):
        # Exclude specific log messages based on their content
        log_message = record.getMessage()
        return not (
            "GET /logs" in log_message and "200" in log_message or
            "GET /" in log_message and "200" in log_message or
            "GET /static/logo.png" in log_message or
            "GET /favicon.ico" in log_message or
            log_message.strip() == '"'  # Exclude empty log lines
        )

# Configure logging
logger = logging.getLogger("BotLogger")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('templates/bot_logs.txt')
file_handler.setLevel(logging.DEBUG)
file_handler.addFilter(IgnoreLogFilter())

# Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.addFilter(IgnoreLogFilter())

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Redirect stdout and stderr to logger
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/logs', methods=['POST', 'GET'])
def get_logs():
    with open("templates/bot_logs.txt", "r") as f:
        logs = f.readlines()
    return jsonify(logs=logs)

def run_site():
    open("templates/bot_logs.txt", "w").close()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
