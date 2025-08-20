from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user
from extensions import db, login_manager
from config import Config
from models import User, Business
# Blueprints

from auth import bp as auth_bp
from admin import bp as admin_bp
from business import bp as biz_bp
from analytics import bp as analytics_bp

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  # Init extensions
  db.init_app(app)
  login_manager.init_app(app)
  # Create tables and seed
  with app.app_context():
    db.create_all()
    seed_admin()
  # Register blueprints
  app.register_blueprint(auth_bp)
  app.register_blueprint(admin_bp)
  app.register_blueprint(biz_bp)
  app.register_blueprint(analytics_bp)
  # Routes

  @app.get("/")
  def index():
    if current_user.is_authenticated:
      return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login"))
  @app.get("/dashboard")
  @login_required
  def dashboard():
    total_users = User.query.count()
    total_businesses = Business.query.count()
    durban_businesses = Business.query.filter_by(city="Durban").count()
    return render_template(
      "dashboard.html",
      total_users=total_users,
      total_businesses=total_businesses,
      durban_businesses=durban_businesses,)
  return app
  
def seed_admin():
  """Seed an initial admin user and some Durban businesses if DB is empty."""
  from config import Config as C
  # Only seed if no users exist yet
  if User.query.first():
    return
  # Admin user
  admin = User(email=C.SEED_ADMIN_EMAIL, is_admin=True)
  admin.set_password(C.SEED_ADMIN_PASSWORD)
  db.session.add(admin)
  # Sample businesses around Durban, KZN
  samples = [
  Business(
    name="Umhlanga Deli",
    category="Food",
    suburb="Umhlanga",
    city="Durban",
    province="KwaZulu-Natal",
    employees=8,
    annual_revenue=1_200_000,
    ),
  Business(
    name="Glenwood Prints",
    category="Services",
    suburb="Glenwood",
    city="Durban",
    province="KwaZulu-Natal",
    employees=4,
    annual_revenue=450_000,
    ),
  Business(
    name="Beachfront Curios",
    category="Retail",
    suburb="North Beach",
    city="Durban",
    province="KwaZulu-Natal",
    employees=6,
    annual_revenue=700_000,
    ),]
  db.session.add_all(samples)
  db.session.commit()

if __name__ == "__main__":
  app = create_app()
  app.run(debug=True)
