from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
id = db.Column(db.Integer, primary_key=True)
email = db.Column(db.String(255), unique=True, nullable=False)
password_hash = db.Column(db.String(255), nullable=False)
is_admin = db.Column(db.Boolean, default=False, nullable=False)
created_at = db.Column(db.DateTime, default=datetime.utcnow)

def set_password(self, password: str):
self.password_hash = generate_password_hash(password)

def check_password(self, password: str) -> bool:
return check_password_hash(self.password_hash, password)

class Business(db.Model):
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(255), nullable=False)
category = db.Column(db.String(120), nullable=False) # e.g., Retail, Food, Services
suburb = db.Column(db.String(120), nullable=True)
city = db.Column(db.String(120), nullable=False)
province = db.Column(db.String(120), nullable=False)
employees = db.Column(db.Integer, default=0)
annual_revenue = db.Column(db.Float, default=0.0) # in ZAR
created_at = db.Column(db.DateTime, default=datetime.utcnow)

def to_dict(self):
return {
"id": self.id,
"name": self.name,
"category": self.category,
"suburb": self.suburb,
"city": self.city,
"province": self.province,
"employees": self.employees,
"annual_revenue": self.annual_revenue,
"created_at": self.created_at.isoformat(),
}
