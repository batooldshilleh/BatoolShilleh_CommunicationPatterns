import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected as listener")

@sio.on("image_progress")
def handle_progress(data):
    print(f"📸 Image {data['image_id']} progress: {data['progress']}% status: {data['status']}")

sio.connect("http://127.0.0.1:5070")

while True:
    time.sleep(1)
