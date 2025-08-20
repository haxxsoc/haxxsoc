from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import User, Business

bp = Blueprint("admin", __name__, url_prefix="/admin")
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required", "warning")
            return redirect(url_for("dashboard"))
        return func(*args, **kwargs)
    return wrapper

@bp.get("/users")
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users.html", users=users)

@bp.post("/users/add")
@login_required
@admin_required
def add_user():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    is_admin = request.form.get("is_admin") == "on"
    if not email or not password:
        flash("Email and password required", "danger")
        return redirect(url_for("admin.users"))
    if User.query.filter_by(email=email).first():
        flash("User already exists", "warning")
        return redirect(url_for("admin.users"))
    u = User(email=email, is_admin=is_admin)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    flash("User added", "success")
    return redirect(url_for("admin.users"))

@bp.post("/users/<int:user_id>/delete")
@login_required
@admin_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash("You cannot delete your own account while logged in.", "warning")
        return redirect(url_for("admin.users"))
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    flash("User deleted", "info")
    return redirect(url_for("admin.users"))

# Business admin
@bp.get("/businesses")
@login_required
@admin_required
def businesses_admin():
    businesses = Business.query.order_by(Business.created_at.desc()).all()
    return render_template("businesses.html", businesses=businesses,admin_mode=True)

@bp.post("/businesses/add")
@login_required
@admin_required
def add_business():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    suburb = request.form.get("suburb", "").strip()
    city = request.form.get("city", "Durban").strip() or "Durban"
    province = request.form.get("province", "KwaZulu-Natal").strip() or "KwaZulu-Natal"
    employees = int(request.form.get("employees", 0) or 0)
    annual_revenue = float(request.form.get("annual_revenue", 0) or 0)

    if not name or not category:
        flash("Name and category are required", "danger")
        return redirect(url_for("admin.businesses_admin"))
    b = Business(
        name=name,
        category=category,
        suburb=suburb or None,
        city=city,
        province=province,
        employees=employees,
        annual_revenue=annual_revenue,
        )
    db.session.add(b)
    db.session.commit()
    flash("Business added", "success")
    return redirect(url_for("admin.businesses_admin"))

@bp.post("/businesses/<int:biz_id>/delete")
@login_required
@admin_required
def delete_business(biz_id):
    b = Business.query.get_or_404(biz_id)
    db.session.delete(b)
    db.session.commit()
    flash("Business deleted", "info")
    return redirect(url_for("admin.businesses_admin"))
