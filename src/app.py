from flask import Flask, render_template, request, redirect, url_for, flash, session

from tcp_serveur import TCPServer
import json

from time import sleep

app = Flask(__name__, template_folder='templates')
server = TCPServer()

@app.route('/')
def index():
    client_data = [{
        'id': client_id,
        'ip': server.client_list[client_id]['socket'].getpeername()[0],
        'port': server.client_list[client_id]['socket'].getpeername()[1],
        'status': 'Active',
        'last_active': 'Just now'  # For demonstration purposes
    } for client_id in server.client_list]
    return render_template('index.html', clients=client_data)

@app.route('/node/<client_id>')
def node_detail(client_id):
    if client_id in server.client_list:
        server.send_message(client_id, 'INFO')
        data = server.recieve_message(client_id)
        print('\n\n\n')
        print(data)
        print('\n\n\n')
        return render_template('node_detail.html', client=json.loads(data))
    else:
        return 'Node not found', 404

if __name__ == '__main__':
    server.run_server()
    app.run()




