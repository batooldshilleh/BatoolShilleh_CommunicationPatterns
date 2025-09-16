from flask import Blueprint, jsonify, request
from app import db, socketio
from app.models import Order, User
import time
from implementations.feature4_restaurant_notifications.routes import notify_new_order

bp = Blueprint('feature2', __name__)


@bp.route("/api/restaurants", methods=["POST"])
def create_restaurant():
    """
    JSON body:
    {
        "name": "<restaurant_name>"
    }
    """
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Restaurant name is required"}), 400

    from app.models import Restaurant

    restaurant = Restaurant(name=name)
    db.session.add(restaurant)
    db.session.commit()

    return jsonify({
        "message": "Restaurant created successfully",
        "restaurant_id": restaurant.id,
        "name": restaurant.name
    }), 201

@bp.route("/api/orders/<int:order_id>/status", methods=["GET"])
def get_order_status(order_id):      
    order = Order.query.get_or_404(order_id)
    last_status = request.args.get("last_status", "")

    timeout = 60
    interval = 1
    start_time = time.time()

    while time.time() - start_time < timeout:
        db.session.refresh(order)
        if order.status != last_status:
            return jsonify({"order_id": order.id, "status": order.status})
        time.sleep(interval)

    return jsonify({"order_id": order.id, "status": order.status})

@bp.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id") 

    from app.models import User, Restaurant
    user = User.query.get(user_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not user or not restaurant:
        return jsonify({"error": "User or Restaurant not found"}), 404

    order = Order(user_id=user_id, restaurant_id=restaurant_id, status="Confirmed")
    db.session.add(order)
    db.session.commit()

   
    notify_new_order(order)

    return jsonify({
        "message": "Order created successfully",
        "order_id": order.id,
        "status": order.status
    }), 201


@bp.route("/api/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    """
    Update the status of an existing order.
    JSON body: { "status": "<new_status>" }
    """
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "Missing status"}), 400

    order.status = new_status
    db.session.commit()
    return jsonify({"order_id": order.id, "status": order.status})
