# DEPENDENCIES
import random
from flask import Flask,render_template,jsonify,session
from flask_socketio import SocketIO,emit,join_room,leave_room,send
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
    def __init__(self,first_user):
        self.users=[]
        self.users.append(first_user)
rooms = {"rooms":[]}

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
    if name not in rooms["rooms"]:
        client_room = room(data["id"])
        session["room"] = client_room
        emit("add_room",{"name":name},broadcast=True)
        rooms["rooms"].append(name)
        rooms[room] = client_room
        emit("start_game",{"name":name})
        join_room(id)
    else:
        emit("room_taken")
@socketio.on("send_name")
def make_name(data):
    session["user"].set_name(data["send_data"])


@socketio.on('get_id')
def get_id():
    id = random.randint(10000000,999999999)
    this_user = user(id)
    session["user"] = this_user
    emit("set_id",{"id":id})
    

@socketio.on('get_rooms')
def get_rooms():
    emit('get_rooms',{"rooms",rooms})
    


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)
