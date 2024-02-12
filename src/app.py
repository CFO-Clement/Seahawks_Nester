import json
import os
import threading

from datetime import datetime
from time import sleep, time
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, flash, request

from tcp_serveur import TCPServer
from logger import Log

log = Log("main")

log.info("Loading environment")
script_dir = os.path.dirname(__file__)
log.debug(f"script_dir: {script_dir}")
env_path = os.path.join(script_dir, '../config.env')
log.debug(f"env_path: {env_path}")
load_dotenv(env_path)

NESTER_LISTEN_IP = os.getenv('NESTER_LISTEN_IP')
NESTER_LISTEN_PORT = int(os.getenv('NESTER_LISTEN_PORT'))

SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_EXPOSE_IP = os.getenv('FLASK_LISTEN_IP')
FLASK_EXPOSE_PORT = int(os.getenv('FLASK_LISTEN_PORT'))

app = Flask(__name__, template_folder='templates')
app.secret_key = SECRET_KEY

stop_event = threading.Event()
server = TCPServer(NESTER_LISTEN_IP, NESTER_LISTEN_PORT, stop_event)

@app.route('/')
def index():
    client_data = [{
        'id': client_id,
        'ip': server.client_list[client_id]['socket'].getpeername()[0],
        'port': server.client_list[client_id]['socket'].getpeername()[1],
        'status': 'Active',
        'last_active': datetime.fromtimestamp(server.client_list[client_id]['last_heartbeat']).strftime('%Y-%m-%d %H:%M:%S')
                if 'last_heartbeat' in server.client_list[client_id] else 'Never'
    } for client_id in server.client_list]
    return render_template('index.html', clients=client_data)


@app.route('/send_heartbeat/<client_id>')
def send_heartbeat(client_id):
    if client_id in server.client_list:
        server.send_message(client_id, 'HEARTBEAT')
        data = server.recieve_message(client_id)
        if data == 'HEARTBEAT':
            flash('Node is responsive', 'success')
        else:
            flash('Node response mismatch', 'warning')
    else:
        flash('Node not found', 'danger')
    return redirect(url_for('index'))


@app.route('/node/<client_id>')
def node_detail(client_id):
    if client_id in server.client_list:
        server.send_message(client_id, 'INFO')
        data = server.recieve_message(client_id)
        return render_template('node_detail.html', data=json.loads(data))
    else:
        return 'Node not found', 404


@app.route('/node_nmap/<client_id>')
def node_nmap(client_id):
    if client_id in server.client_list:
        return render_template('node_nmap.html', client_id=client_id)
    else:
        return 'Node not found', 404


@app.route('/run_nmap/<client_id>', methods=['POST'])
def run_nmap(client_id):
    if client_id not in server.client_list:
        return 'Node not found', 404

    target = request.form['target']
    predefined = request.form['predefined_command'].replace('+', ' ')
    custom = request.form['custom_command']
    command = f"NMAP {predefined} {target}" if predefined else f"NMAP {custom}"
    server.send_message(client_id, command)
    data = server.recieve_message(client_id)

    if data:
        data = json.loads(data)
        return render_template('nmap_results.html', data=data)
    else:
        return 'No data received', 404


if __name__ == '__main__':
    log.info(f"Starting server on {NESTER_LISTEN_IP}:{NESTER_LISTEN_PORT}")
    try:
        server.run_server()
        sleep(1)
        if stop_event.is_set():
            log.critical("Server failed to start")
            raise Exception("Server failed to start")
        #server.start_heartbeat_thread()
        app.run(debug=False, host=FLASK_EXPOSE_IP, port=FLASK_EXPOSE_PORT)
    except Exception as e:
        log.critical(f"Unhandled exception: {e}")
        log.warning("Closing server and exiting")
        server.broadcast_message('CLOSE')
        server._critical_fail("Unhandled exception")
        sleep(1)
        exit(1)

