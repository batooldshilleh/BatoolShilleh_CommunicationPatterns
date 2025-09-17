# file: implementations/feature3_driver_location/routes.py
from flask import Blueprint
from flask_socketio import SocketIO, join_room, leave_room, emit
from app.models import Order
from app import db, socketio

bp = Blueprint('feature3', __name__)

@socketio.on("join_order_room")
def join_order(data):
    print("join_order_room received:", data)
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    order = Order.query.get(order_id)

    if order is None or order.user_id != user_id:
        emit("error", {"message": "Unauthorized or invalid order"})
        return

    room = f"order_{order_id}"
    join_room(room)
    emit("joined", {"message": f"Joined room for order {order_id}"})

@socketio.on("leave_order_room")
def leave_order(data):
    order_id = data.get("order_id")
    room = f"order_{order_id}"
    leave_room(room)
    emit("left", {"message": f"Left room for order {order_id}"})

@socketio.on("update_driver_location")
def update_driver_location(data):
    print("update_driver_location received:", data)
    order_id = data.get("order_id")
    lat = data.get("lat")
    lng = data.get("lng")

    order = Order.query.get(order_id)
    if not order:
        emit("error", {"message": "Order not found"})
        return

    room = f"order_{order_id}"
    emit("driver_location", {"lat": lat, "lng": lng}, room=room)
