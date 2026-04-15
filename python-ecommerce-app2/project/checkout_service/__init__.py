from flask import Blueprint

# 1. Create the blueprint
checkout_bp = Blueprint('checkout', __name__)

# 2. Import the routes
from . import routes
