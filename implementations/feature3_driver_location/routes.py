from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
from app.models import Order, Driver
from app import db, socketio

bp = Blueprint('feature3', __name__)

# WebSocket namespace for driver location updates
@socketio.on("join_order_room")
def join_order(data):
    """
    Customer joins the room to receive driver location updates.
    data = {"order_id": int, "user_id": int}
    """
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

# Driver sends location updates
@socketio.on("update_driver_location")
def update_driver_location(data):
    """
    data = {"order_id": int, "lat": float, "lng": float}
    """
    order_id = data.get("order_id")
    lat = data.get("lat")
    lng = data.get("lng")

    order = Order.query.get(order_id)
    if not order:
        emit("error", {"message": "Order not found"})
        return

    room = f"order_{order_id}"
    # Broadcast location to the customer in this room
    emit("driver_location", {"lat": lat, "lng": lng}, room=room)
