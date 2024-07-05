import os
import socket
import logging

import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys
from termcolor import cprint


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except requests.RequestException as e:
        logger.error(f"Error fetching public IP: {e}")
        return None


cprint(f"Running Site... IP: {socket.gethostbyname(socket.gethostname())}/{get_public_ip()}", "light_green")
# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Custom logging handler
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit('log', {'msg': log_entry})

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create and add handler to logger
socketio_handler = SocketIOHandler()
socketio_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
socketio_handler.setFormatter(formatter)
logger.addHandler(socketio_handler)

# Redirect stdout and stderr
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    cprint("Running main...", "light_green")
    exec(open('main.py').read())

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
