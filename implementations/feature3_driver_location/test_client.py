import socketio


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

@sio.on("driver_location")
def on_location(data):
    print("Driver location:", data)

@sio.on("error")
def on_error(data):
    print("Error:", data)

sio.connect("http://127.0.0.1:8000")

sio.emit("join_order_room", {"order_id": 2, "user_id": 1})

sio.emit("update_driver_location", {"order_id": 2, "lat": 40.7128, "lng": -74.0060})

import time
time.sleep(10)

sio.disconnect()
