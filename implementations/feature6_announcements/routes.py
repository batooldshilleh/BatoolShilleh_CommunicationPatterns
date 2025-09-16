from flask import Blueprint, request, jsonify
from app import db
from app.models import Announcement
import os
import redis
from rq import Queue
from implementations.feature6_announcements.worker import process_announcement

bp = Blueprint("feature6", __name__, url_prefix="/api/announcements")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = redis.from_url(REDIS_URL)
q = Queue("default", connection=redis_conn)

@bp.route("", methods=["POST"])
def create_announcement():
    data = request.get_json() or {}
    title = data.get("title")
    body = data.get("body")
    urgent = bool(data.get("urgent", False))

    if not title or not body:
        return jsonify({"error": "title and body are required"}), 400

    ann = Announcement(title=title, body=body, urgent=urgent)
    db.session.add(ann)
    db.session.commit()

    q.enqueue(process_announcement, ann.id)

    return jsonify({
        "message": "Announcement created and queued for broadcast",
        "announcement_id": ann.id
    }), 201

@bp.route("", methods=["GET"])
def list_announcements():
    anns = Announcement.query.order_by(Announcement.created_at.desc()).limit(50).all()
    items = [{"id": a.id, "title": a.title, "body": a.body, "created_at": a.created_at.isoformat(), "broadcasted": a.broadcasted} for a in anns]
    return jsonify(items)
