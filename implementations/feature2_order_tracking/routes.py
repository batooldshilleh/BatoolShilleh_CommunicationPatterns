from flask import Blueprint, jsonify, request
from app import db, socketio
from app.models import Order, User
import time
from implementations.feature4_restaurant_notifications.routes import notify_new_order

bp = Blueprint('feature2', __name__)

# Long Polling status
@bp.route("/api/orders/<int:order_id>/status", methods=["GET"])
def get_order_status(order_id):  # ← يجب أن يكون order_id هنا
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

# Create new order
@bp.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")  # يجب تمرير المطعم
    order = Order(user_id=user_id, restaurant_id=restaurant_id, status="Confirmed")
    db.session.add(order)
    db.session.commit()

    # أرسل إشعار للموظفين
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
