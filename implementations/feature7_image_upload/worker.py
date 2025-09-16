import time
import os
from PIL import Image
from app import create_app, db, socketio
from app.models import MenuItemImage

app = create_app()

UPLOAD_FOLDER = "uploads/processed"

def process_image(image_id):
    with app.app_context():
        img = MenuItemImage.query.get(image_id)
        if not img:
            return

        img.status = "processing"
        img.progress = 0
        db.session.commit()

        input_path = os.path.join("uploads", img.filename)
        output_path = os.path.join(UPLOAD_FOLDER, img.filename)

        try:
            # Simulate processing
            total_steps = 5
            for step in range(1, total_steps + 1):
                time.sleep(5)  # each step ~5s, adjust to real processing
                img.progress = int((step / total_steps) * 100)
                db.session.commit()
                # Notify clients via SocketIO
                socketio.emit(
                    "image_progress",
                    {"image_id": img.id, "progress": img.progress, "status": img.status},
                    namespace="/"
                )

            # Open, resize, compress using PIL
            with Image.open(input_path) as im:
                im.thumbnail((800, 800))
                im.save(output_path, optimize=True, quality=85)

            img.status = "done"
            img.progress = 100
            db.session.commit()
            socketio.emit(
                "image_progress",
                {"image_id": img.id, "progress": img.progress, "status": img.status},
                namespace="/"
            )
        except Exception as e:
            img.status = "failed"
            db.session.commit()
            socketio.emit(
                "image_progress",
                {"image_id": img.id, "progress": img.progress, "status": img.status},
                namespace="/"
            )
