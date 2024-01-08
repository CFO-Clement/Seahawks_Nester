from flask import Flask, render_template, request, redirect, url_for, flash, session

from tcp_serveur import TCPServer

app = Flask(__name__, template_folder='templates')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    #app.run()
    server = TCPServer()
    server.start()

