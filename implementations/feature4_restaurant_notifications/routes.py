from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room
from app.models import Order, Restaurant
from app import db, socketio

bp = Blueprint('feature4', __name__)

@socketio.on("join_restaurant_room")
def join_restaurant(data):
    """
    data = {"restaurant_id": int, "staff_id": int}
    """
    restaurant_id = data.get("restaurant_id")
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        emit("error", {"message": "Invalid restaurant"})
        return

    room = f"restaurant_{restaurant_id}"
    join_room(room)
    emit("joined", {"message": f"Joined restaurant {restaurant_id} room"})

@socketio.on("leave_restaurant_room")
def leave_restaurant(data):
    restaurant_id = data.get("restaurant_id")
    room = f"restaurant_{restaurant_id}"
    leave_room(room)
    emit("left", {"message": f"Left restaurant {restaurant_id} room"})

def notify_new_order(order):
    """
    order: Order instance
    """
    room = f"restaurant_{order.restaurant_id}"
    emit("new_order", {
        "order_id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "created_at": str(order.created_at)
    }, room=room)
