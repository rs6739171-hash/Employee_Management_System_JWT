from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)

from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            token = create_access_token(identity=str(user.id))
            response = redirect(url_for("employee.home"))
            set_access_cookies(response, token)
            return response

        return render_template(
            "login.html",
            error="Invalid username or password",
        )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required",
        }), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid username or password",
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "expires_in": "1 hour",
    })


@auth_bp.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
    })
