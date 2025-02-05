from flask import Flask
from .users import users_bp
from .items import items_bp

def register_all_blueprints(app: Flask):
    """Register all blueprint to the Flask app"""
    app.register_blueprint(users_bp, url_prefix="/api")
    app.register_blueprint(items_bp, url_prefix="/api/items")

