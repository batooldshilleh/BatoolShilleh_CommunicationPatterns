import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected as listener")

@sio.on("announcement")
def handle_announcement(data):
    print("📢 Announcement:", data)

sio.connect("http://127.0.0.1:5070")

while True:
    time.sleep(1)
