import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000')


def log_message(message: str) -> None:
    sio.emit('log', message)
    print(message)
