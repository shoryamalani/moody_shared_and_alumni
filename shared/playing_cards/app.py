# DEPENDENCIES
import random
from flask import Flask,render_template,jsonify,session
from flask_socketio import SocketIO,emit,join_room,leave_room
#https://flask-socketio.readthedocs.io/en/latest/

#APP STUFF
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

class user:
    def __init__(self,id):
        self.user_id = id
    def set_name(self,name):
        self.name = name 

class room:
    def __init__(self,id,first_user):
        self.id = id
        self.users=[]
        self.users.append(first_user)
rooms = []

#ROUTERS
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

#SOCKET HANDLERS
# @socketio.on('send_data')
# def send_back(data):
#     emit("send_data_back",{
#         "data":data["data_sent"]
#     },broadcast=True)

@socketio.on("create_room")
def create_room(data):
    name = data["data"]
    id = random.randint(10000,99999)
    client_room = room(id,data["id"])
    session["room"] = client_room
    emit("add_room",{"name":name},broadcast=True)

@socketio.on("send_name")
def make_name(data):
    session["user"].set_name(data["send_data"])


# This is for if we ever need ids. i accidentally made it not realizing we don't need it and can just use session.
@socketio.on('get_id')
def get_id():
    id = random.randint(10000000,999999999)
    this_user = user(id)
    session["user"] = this_user
    emit("set_id",{"id":id})


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)
