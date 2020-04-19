# DEPENDENCIES
import random
from flask import Flask,render_template,jsonify,session,g
from flask_socketio import SocketIO,emit,join_room,leave_room,send
import james_bond
import blackjack
#https://flask-socketio.readthedocs.io/en/latest/

#APP STUFF
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

#Classes
class user:
    def __init__(self,id):
        self.user_id = id
    def set_name(self,name):
        self.name = name 

class room:
    def __init__(self,first_user):
        self.users=[]
        self.users.append(first_user)
    def add_member(self,id):
        self.users.append(id)
    def initialize_game(self,game):
        self.game = game
        if game == "james_bond":
            pass
        elif game == "blackjack":
            pass#set up blackjack things
    
#Globals
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
        player_name = session.get("name") if session.get("name") else data["id"]
        client_room = room(player_name)
        session["room"] = client_room
        emit("add_room",{"name":name},broadcast=True)
        rooms["rooms"].append(name)
        rooms[name] = client_room
        emit("start_game",{"name":name})
        join_room(name)
    else:
        emit("room_taken")

@socketio.on("join_room")
def joining_room(data):
    room_to_join = rooms[data["name"]]
    name = session.get("name") if session.get("name") else data["id"]
    room_to_join.add_member(name)
    join_room(data["name"])
    session["room"] = room_to_join
    player_name = session.get("name") if session.get("name") else data["id"]
    emit("new_player",{"name":player_name},room=data["name"])
    emit("join_game",{"players":room_to_join.users},room=data["name"])

@socketio.on("choose_game")
def choose_game(data):
    room = session.get("room")
    room.initialize_game(data["game"])
    

@socketio.on("send_name")
def make_name(data):
    session["name"] = data["data_sent"]
    session["user"].set_name(data["data_sent"])


@socketio.on('get_id')
def get_id():
    id = random.randint(10000000,999999999)
    this_user = user(id)
    session["user"] = this_user
    emit("set_id",{"id":id})
    

@socketio.on('get_rooms')
def get_rooms():
    emit('get_rooms',{"rooms":rooms["rooms"]})
    


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)
