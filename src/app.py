import json
from time import sleep

from flask import Flask, render_template, redirect, url_for, flash, request

from tcp_serveur import TCPServer

app = Flask(__name__, template_folder='templates')
app.secret_key = 'une_cle_secrete_tres_complexe'
server = TCPServer()


@app.route('/')
def index():
    client_data = [{
        'id': client_id,
        'ip': server.client_list[client_id]['socket'].getpeername()[0],
        'port': server.client_list[client_id]['socket'].getpeername()[1],
        'status': 'Active',
        'last_active': server.client_list[client_id]['last_active'] if 'last_active' in server.client_list[client_id] else 'Never'
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

    command = request.form['command']
    server.send_message(client_id, command)
    data = server.recieve_message(client_id)

    if data:
        data = json.loads(data)
        return render_template('nmap_results.html', data=data)
    else:
        return 'No data received', 404


if __name__ == '__main__':
    try:
        server.run_server()
        sleep(1)
    except Exception as e:
        print('Server stopping...')
        server.broadcast_message('KILL')
        sleep(1)
        exit(0)
    else:
        #pass
        app.run(debug=False)
