import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on("status")
def on_status(data):
    print("Status:", data)

@sio.on("new_message")
def on_new_message(data):
    print("New message received:", data)

@sio.on("typing")
def on_typing(data):
    print("Typing:", data)

@sio.on("delivered_ack")
def on_delivered_ack(data):
    print("Delivered ack:", data)

# Connect to server
sio.connect("http://127.0.0.1:5070")

# Join a chat room
sio.emit("join_chat", {"room_id": 1, "user_type": "customer"})

# Send a test message
sio.emit("send_message", {"room_id": 1, "sender_type": "customer", "content": "Hello, I need help!"})

# Simulate typing
sio.emit("typing", {"room_id": 1, "user_type": "customer"})

# Simulate delivery acknowledgment (replace with actual message id if known)
# sio.emit("delivered", {"message_id": 1})

# Keep the client running to receive events
time.sleep(60)
sio.disconnect()
