# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
from flask_socketio import SocketIO, send, emit

import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_random_color():
    tmp = '0123456789abcdef'
    tmp_list = list(tmp)
    random.shuffle(tmp_list)
    color = '#' + ''.join(tmp_list[0:6])
    return color

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

@socketio.on('message')
def handle_message(message):
    msg = json.loads(message)
    data = dict(
        msg = msg.get('msg'),
        nickname = msg.get('nickname')
    )

    if not session.get('bgcolor'):
        session['bgcolor'] = get_random_color()
    
    data['color'] = session['bgcolor']
    data = json.dumps(data)
    # emit('message', {'data': data})
    send({'data': data})

# web terminal
@app.route('/xterm')
def xterm():
    return render_template('terminal.html')

@socketio.on('connect', namespace='/terminal')
def handle_terminal_connect():
    emit('message', {'data': 'Connected'})


@socketio.on('message', namespace='/terminal')
def handle_terminal_message(msg):
    print('=====>', msg)
    emit('message', {'data': msg})
    
if __name__ == '__main__':
    socketio.run(app, debug=True)