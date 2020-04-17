from flask import Flask,render_template,jsonify
from flask_login import current_user
from flask_socketio import SocketIO,emit,join_room,leave_room
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('send_data')
def send_back(data):
    emit("send_data_back",{
        "data":data["data_sent"]
    },broadcast=True)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)