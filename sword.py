from flask import Flask, render_template, jsonify
from flask.ext.socketio import SocketIO, leave_room, join_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('join_room', namespace='/soc')
def join_to_room(msg):
	room = msg['room_id']
	emit('joined', {'msg': "ready"}, room=room)

@socketio.on('room_create', namespace='/soc')
def room_create(msg):
	room = msg['room_id']
	join_room(room)
	emit('created', {"msg": "ready"}, room=room)

@socketio.on('orientation_change', namespace='/soc')
def orientation_change(msg):
	emit('position_change', msg, room=msg['room_id'])

@socketio.on("on_off", namespace='/soc')
def on_off(msg):
	emit('sword_off_on', msg, room=msg['room_id'])


@app.route('/')
def index():
	return render_template('webgl.html')

@app.route('/<id>')
def joined_index(id): 
	return render_template("join.html", room_id = id)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80)
