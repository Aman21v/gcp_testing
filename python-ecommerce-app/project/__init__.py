import os
from flask import Flask
from .extensions import redis_client



def create_app():
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # A strong secret key is crucial for session security
    )
   # Initialize extensions with the app context
    redis_client.init_app(app)


    with app.app_context():
        # --- CORRECTED IMPORTS FOR ALL SERVICES ---
        from .frontend_service import frontend_bp
        from .product_service import product_bp   # Corrected
        from .cart_service import cart_bp         # Corrected
        from .checkout_service import checkout_bp # Corrected
        from .ad_service import ad_bp             # Corrected
        
        # Register the blueprints
        app.register_blueprint(frontend_bp)
        app.register_blueprint(product_bp)
        app.register_blueprint(cart_bp)
        app.register_blueprint(checkout_bp)
        app.register_blueprint(ad_bp)
        
        print("Application created and all blueprints registered successfully.")

    return app
