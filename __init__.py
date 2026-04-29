from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'   # redirect to login


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import models (IMPORTANT)
    from app.models import User

    # Import routes
    from app.routes import main
    app.register_blueprint(main)

    # Create tables + default admin
    with app.app_context():
        db.create_all()
        create_default_admin()

    return app


# 🔐 Create default admin
def create_default_admin():
    from app.models import User   # import here also (safe)

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')   # ⚠️ change later

        db.session.add(admin)
        db.session.commit()

        print("✅ Default admin created: admin / admin123")