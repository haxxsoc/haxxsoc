from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func, extract
from extensions import db
from models import Business
bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@bp.get("")
@login_required
def view_analytics():
  # Count by category
  by_category = db.session.query(Business.category, func.count(Business.id)).group_by(Business.category).all()

  # Count by suburb (only non-null)
  by_suburb = db.session.query(Business.suburb, func.count(Business.id)).filter(Business.suburb.isnot(None)).group_by(Business.suburb).order_by(func.count(Business.id).desc()).limit(12).all()

  # New businesses per month (last 12 months)
  month_counts = db.session.query(
  extract('year', Business.created_at).label('y'),
  extract('month', Business.created_at).label('m'),
    func.count(Business.id)).group_by('y','m').order_by('y','m').all()


  # Prepare data for charts
  cat_labels = [c for c,_ in by_category]
  cat_values = [int(n) for _,n in by_category]
  
  sub_labels = [s or "Unknown" for s,_ in by_suburb]
  sub_values = [int(n) for _,n in by_suburb]
  
  # Format months as YYYY-MM
  month_labels = [f"{int(y):04d}-{int(m):02d}" for y,m,_ in month_counts]
  month_values = [int(n) for *_, n in month_counts]
  
  totals = {
    "total_businesses": db.session.query(func.count(Business.id)).scalar() or 0,
    "total_employees": db.session.query(func.coalesce(func.sum(Business.employees), 0)).scalar() or 0,
    "total_revenue": db.session.query(func.coalesce(func.sum(Business.annual_revenue), 0.0)).scalar() or 0.0,}
  
  return render_template(
    "analytics.html",
    cat_labels=cat_labels, cat_values=cat_values,
    sub_labels=sub_labels, sub_values=sub_values,
    month_labels=month_labels, month_values=month_values,
    totals=totals,)
