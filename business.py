from flask import Blueprint, render_template
from flask_login import login_required
from models import Business

bp = Blueprint("biz", __name__, url_prefix="/businesses")

@bp.get("")
@login_required
def list_businesses():
  businesses = Business.query.order_by(Business.created_at.desc()).all()
  return render_template("businesses.html", businesses=businesses, admin_mode=False)
