from flask import Blueprint

# 1. Create the blueprint
ad_bp = Blueprint('ad', __name__)

# 2. Import the routes
from . import routes
