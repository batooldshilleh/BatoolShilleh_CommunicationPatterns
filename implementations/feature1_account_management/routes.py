from flask import Blueprint, request, jsonify
from app import db
from app.models import User

bp = Blueprint('feature1', __name__)

# Register
@bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

# Login
@bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful", "user_id": user.id})

# Update Profile
@bp.route("/api/auth/update-profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    if "username" in data:
        user.username = data["username"]
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})
