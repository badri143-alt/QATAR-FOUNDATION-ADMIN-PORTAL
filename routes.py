from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Opportunity

bp = Blueprint("bp", __name__)

ALLOWED = [
    "Technology",
    "Business",
    "Design",
    "Marketing",
    "Data Science",
    "Other"
]

# SIGNUP
@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not full_name or not email or not password or not confirm_password:
        return jsonify({"error": "All fields required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    existing = Admin.query.filter_by(email=email).first()

    if existing:
        return jsonify({"error": "Account already exists"}), 409

    user = Admin(
        full_name=full_name,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


# LOGIN
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    remember = data.get("remember_me", False)

    user = Admin.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user, remember=remember)

    return jsonify({"message": "Login successful"})


# LOGOUT
@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})


# GET OPPORTUNITIES
@bp.route("/opportunities", methods=["GET"])
@login_required
def get_opportunities():
    ops = Opportunity.query.filter_by(admin_id=current_user.id).all()

    result = []

    for op in ops:
        result.append({
            "id": op.id,
            "name": op.name,
            "duration": op.duration,
            "start_date": op.start_date,
            "description": op.description,
            "skills": op.skills,
            "category": op.category,
            "future_opportunities": op.future_opportunities,
            "max_applicants": op.max_applicants
        })

    return jsonify(result)


# ADD OPPORTUNITY
@bp.route("/opportunities", methods=["POST"])
@login_required
def add_opportunity():
    data = request.get_json()

    op = Opportunity(
        name=data.get("name"),
        duration=data.get("duration"),
        start_date=data.get("start_date"),
        description=data.get("description"),
        skills=data.get("skills"),
        category=data.get("category"),
        future_opportunities=data.get("future_opportunities"),
        max_applicants=data.get("max_applicants"),
        admin_id=current_user.id
    )

    db.session.add(op)
    db.session.commit()

    return jsonify({"message": "Opportunity created"})

# EDIT OPPORTUNITY
@bp.route("/opportunities/<int:id>", methods=["PUT"])
@login_required
def edit_opportunity(id):
    op = Opportunity.query.filter_by(id=id, admin_id=current_user.id).first()

    if not op:
        return jsonify({"error": "Opportunity not found"}), 404

    data = request.get_json()

    op.name = data.get("name")
    op.duration = data.get("duration")
    op.start_date = data.get("start_date")
    op.description = data.get("description")
    op.skills = data.get("skills")
    op.category = data.get("category")
    op.future_opportunities = data.get("future_opportunities")
    op.max_applicants = data.get("max_applicants")

    db.session.commit()

    return jsonify({"message": "Updated successfully"})


# DELETE OPPORTUNITY
@bp.route("/opportunities/<int:id>", methods=["DELETE"])
@login_required
def delete_opportunity(id):
    op = Opportunity.query.filter_by(id=id, admin_id=current_user.id).first()

    if not op:
        return jsonify({"error": "Opportunity not found"}), 404

    db.session.delete(op)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})