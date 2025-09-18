import os
import logging
from flask import Flask
from extensions import db

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mental-health-companion-secret-key-2025")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///mental_health_companion.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import models and routes after app and db setup
with app.app_context():
    import models  # noqa: F401
    import routes  # noqa: F401
    
    db.create_all()
