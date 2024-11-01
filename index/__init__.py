from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Initialize the LoginManager instance
login_manager = LoginManager()

# Function to initialize the core app
def create_app():
    app = Flask(__name__)

    # Configure app
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for the database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize the database with the app
    db.init_app(app)

    # Initialize the LoginManager with the app
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Redirect to login page if not logged in

    # User loader callback for Flask-Login
    from .models import User  # Import the User model here
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Retrieve user by ID for Flask-Login

    # Import and register blueprints or routes
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
