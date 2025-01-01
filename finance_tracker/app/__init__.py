from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from config.config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    cache.init_app(app)
    
    # Import models - Add this section
    from app.models.user import User
    from app.models.transaction import Transaction
    from app.models.budget import Budget
    from app.models.savings_goal import SavingsGoal
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.transaction import transaction_bp
    from app.routes.budget import budget_bp
    from app.routes.analytics import analytics_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(budget_bp, url_prefix='/api/budgets')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    # Setup logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/finance_tracker.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Finance Tracker startup')
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app