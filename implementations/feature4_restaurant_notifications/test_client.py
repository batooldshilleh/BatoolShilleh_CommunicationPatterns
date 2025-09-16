import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on("joined")
def on_joined(data):
    print("Joined room:", data)

@sio.on("new_order")
def on_new_order(data):
    print("New order received:", data)

@sio.on("error")
def on_error(data):
    print("Error:", data)

sio.connect("http://127.0.0.1:5070")

sio.emit("join_restaurant_room", {"restaurant_id": 1, "staff_id": 1})

time.sleep(60)

sio.disconnect()
