from flask import Blueprint

# Create blueprint instances
auth_bp = Blueprint('auth', __name__)
transaction_bp = Blueprint('transaction', __name__)
budget_bp = Blueprint('budget', __name__)
analytics_bp = Blueprint('analytics', __name__)

# Import routes AFTER blueprint creation
# These imports must be after the blueprint creation to avoid circular imports
from app.routes.auth import *
from app.routes.transaction import *
from app.routes.budget import *
from app.routes.analytics import *

# Export the blueprints