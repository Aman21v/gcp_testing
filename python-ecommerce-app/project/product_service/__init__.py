from flask import Blueprint

# 1. Create the blueprint
product_bp = Blueprint('product', __name__)

# 2. Import the routes
from . import routes
