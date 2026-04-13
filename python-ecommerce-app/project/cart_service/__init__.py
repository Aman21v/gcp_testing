from flask import Blueprint

# 1. Create the blueprint
cart_bp = Blueprint('cart', __name__)

# 2. Import the routes
from . import routes
