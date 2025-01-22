import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta

# Initialize extensions
# These will be attached to the app instance later
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    """
    Application Factory for creating the Flask app instance.
    This pattern is useful for managing configurations and testing.
    """
    app = Flask(__name__)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://strider:a@localhost/mt')  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Improves performance by disabling event tracking
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')  # Use a secure default in development
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=20)  # Customize token expiry time


        
    

    # Initialize extensions with the app instance
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are registered with Flask-Migrate
    from .models import User, Goal, FoodEntry

    # Register blueprints for modular routes
    from .routes import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    return app

# Create and expose the app instance
app = create_app()
