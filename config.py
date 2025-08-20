import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-dev-secret")
SQLALCHEMY_DATABASE_URI = os.getenv(
"DATABASE_URL",
f"sqlite:///{os.path.join(BASE_DIR, 'bizdash.db')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Seed admin (only used if DB empty on first run)
SEED_ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "admin@example.com")
SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "admin123")
CITY_DEFAULT = "Durban"
PROVINCE_DEFAULT = "KwaZulu-Natal"
