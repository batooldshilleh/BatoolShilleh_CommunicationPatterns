from app import create_app, socketio
from implementations.feature1_account_management.routes import bp as feature1_bp
from implementations.feature2_order_tracking.routes import bp as feature2_bp
from implementations.feature3_driver_location.routes import bp as feature3_bp
from implementations.feature4_restaurant_notifications.routes import bp as feature4_bp
from implementations.feature5_customer_support_chat.routes import bp as chat_bp
from implementations.feature6_announcements.routes import bp as feature6_bp   
from implementations.feature7_image_upload.routes import bp as feature7_bp

app = create_app()

# Register feature blueprints
app.register_blueprint(feature1_bp)
app.register_blueprint(feature2_bp)
app.register_blueprint(feature3_bp)
app.register_blueprint(feature4_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(feature6_bp)  
app.register_blueprint(feature7_bp)
if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5070, debug=True, allow_unsafe_werkzeug=True)
