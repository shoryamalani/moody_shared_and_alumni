from flask import Flask,render_template
from flask_socketio import SocketIO,emit,join_room,leave_room
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socket.̨

if __name__ == '__main__':
    socketio.run(app,debug=True)