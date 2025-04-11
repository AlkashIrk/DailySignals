from flask_socketio import send, emit, SocketIO

from flask_app.flask_data import prepare_instruments, prepare_candles, prepare_candles_ticker


def init_messages(socketio: SocketIO):
    @socketio.on('message')
    def handle_message(msg):
        print('Message: ' + msg)
        send(msg, broadcast=True)

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('broadcast')
    def handle_broadcast_event(msg):
        send(msg, broadcast=True)

    @socketio.on('update')
    def handle_update_event(data):
        if data == '/instruments':
            handle_custom_event_instruments(data)
        elif data == '/candles':
            handle_custom_event_candles()
        elif '/candles/' in data:
            ticker = data[9:]
            handle_custom_event_candles(ticker)

    def handle_custom_event_candles(ticker=None):
        if ticker is None:
            df = prepare_candles()
        else:
            df = prepare_candles_ticker(ticker)
        records = df.to_dict('records')
        for r in records:
            emit('update', r, broadcast=False)

    def handle_custom_event_instruments(data):
        df = prepare_instruments()
        records = df.to_dict('records')
        for r in records:
            emit('update', r, broadcast=False)
