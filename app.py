from flask import Flask, jsonify, redirect, request, url_for

from config import Config
from extensions import db, jwt
from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from auth_routes import auth_bp
    from employee_routes import employee_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        if request.path.startswith("/api/"):
            return jsonify({"error": "JWT token is required"}), 401
        return redirect(url_for("auth.login"))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        if request.path.startswith("/api/"):
            return jsonify({
                "error": "JWT token has expired. Please login again.",
            }), 401
        return redirect(url_for("auth.login"))

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Invalid JWT token"}), 401
        return redirect(url_for("auth.login"))

    with app.app_context():
        db.create_all()

        username = app.config["ADMIN_USERNAME"]
        password = app.config["ADMIN_PASSWORD"]
        admin = User.query.filter_by(username=username).first()

        if not admin:
            admin = User(username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()

    return app
