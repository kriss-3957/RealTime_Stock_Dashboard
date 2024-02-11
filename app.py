from flask import Flask, render_template
from flask_socketio import SocketIO
import api

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    data = api.convertWatchlist()
    return render_template('index.html', data=data)

@socketio.on('update_symbol')
def handle_update_symbol(data):
    socketio.emit('update_symbol', {'symbol': data['symbol']}, broadcast=True)

# if __name__ == '__main__':
#     # Use SocketIO's run method instead of app.run
#     socketio.run(app, debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
