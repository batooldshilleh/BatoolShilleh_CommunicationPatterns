from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import MenuItemImage
import redis
from rq import Queue
from implementations.feature7_image_upload.worker import process_image

bp = Blueprint("feature7", __name__, url_prefix="/api/menu-images")

REDIS_URL = "redis://localhost:6379"
redis_conn = redis.from_url(REDIS_URL)
q = Queue("default", connection=redis_conn)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Create DB entry
    img = MenuItemImage(restaurant_id=1, filename=filename)  # replace restaurant_id dynamically
    db.session.add(img)
    db.session.commit()

    # Enqueue processing
    q.enqueue(process_image, img.id)

    return jsonify({"image_id": img.id, "status": img.status}), 201

@bp.route("/status/<int:image_id>", methods=["GET"])
def get_status(image_id):
    img = MenuItemImage.query.get(image_id)
    if not img:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "image_id": img.id,
        "status": img.status,
        "progress": img.progress
    })
