from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# 🚗 VIOLATION MODEL
# =========================
class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False, index=True)
    violation_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    fine_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Unpaid')  # Unpaid / Paid
    qr_code_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Violation {self.vehicle_number} - {self.status}>"


# =========================
# 👤 USER MODEL
# =========================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # 🔐 Set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 🔍 Check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"