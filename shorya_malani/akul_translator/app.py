import random
from flask import Flask,render_template,jsonify,session,g
from flask_socketio import SocketIO,emit,join_room,leave_room,send

#APP STUFF
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

#GLOBALS
akul_taken = {"taken":False,"translations":["binkadoo"],"binkadoo":"bad"}


#ROUTERS
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on("i_am_akul")
def i_am_akul():
    if akul_taken["taken"] != True:
        socketio.emit("akul_accepted")
        akul_taken["taken"] = True
    else:
        socketio.emit("akul_denied")
@socketio.on("akul_talking")
def akul_talking(data):
    string_of_akul = data["words"]
    print(string_of_akul)
    final_string = string_of_akul
    for translate in akul_taken["translations"]:
        if translate in string_of_akul:
            final_string = final_string.replace(translate,akul_taken[translate])      
    socketio.emit("akul_says",{"akul_raw":string_of_akul,"final_string":final_string},broadcast=True)
    
    



if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)
    
    