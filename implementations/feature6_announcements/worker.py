# worker.py
from app import create_app, db, socketio
from app.models import Announcement

app = create_app()

def process_announcement(ann_id):
    with app.app_context():
        ann = Announcement.query.get(ann_id)
        if not ann:
            return
        # طريقة آمنة للبث لكل المستخدمين
        socketio.emit(
            "announcement",
            {"id": ann.id, "title": ann.title, "body": ann.body},
            namespace="/"
        )
        ann.broadcasted = True
        db.session.commit()
