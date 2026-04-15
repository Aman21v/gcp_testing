from flask import Blueprint

# 1. Create the blueprint
frontend_bp = Blueprint('frontend', __name__)

# 2. Import the routes to register them with the blueprint
from . import routes
