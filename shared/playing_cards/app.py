# DEPENDENCIES
import random
from flask import Flask,render_template,jsonify,session
from flask_socketio import SocketIO,emit,join_room,leave_room

#APP STUFF
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
async_mode = None

class user:
    def __init__(self,id):
        self.user_id = id
    def set_name(self,name):
        self.name = name 
#ROUTERS
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

#SOCKET HANDLERS
@socketio.on('send_data')
def send_back(data):
    emit("send_data_back",{
        "data":data["data_sent"]
    },broadcast=True)

# This is for if we ever need ids. i accidentally made it not realizing we don't need it and can just use session.
# @socketio.on('get_id')
# def get_id():
#     id = random.randint(10000000,999999999)
#     this_user = user(id)
#     session["user"] = this_user
#     emit("send_id",{"id":id})

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)