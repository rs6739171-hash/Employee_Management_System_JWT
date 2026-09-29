from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models import Employee

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/")
@jwt_required()
def home():
    search = request.args.get("search", "").strip()

    if search:
        employees = Employee.query.filter(
            (Employee.name.contains(search))
            | (Employee.employee_id.contains(search))
            | (Employee.department.contains(search))
        ).all()
    else:
        employees = Employee.query.order_by(Employee.id.desc()).all()

    return render_template(
        "index.html",
        employees=employees,
        search=search,
    )


@employee_bp.route("/add", methods=["GET", "POST"])
@jwt_required()
def add_employee():
    if request.method == "POST":
        employee = Employee(
            employee_id=request.form["employee_id"].strip(),
            name=request.form["name"].strip(),
            email=request.form["email"].strip().lower(),
            phone=request.form["phone"].strip(),
            department=request.form["department"],
            designation=request.form["designation"].strip(),
            salary=float(request.form["salary"]),
        )

        try:
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for("employee.home"))
        except Exception:
            db.session.rollback()
            return "Employee ID or Email already exists."

    return render_template("add_employee.html")


@employee_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@jwt_required()
def edit_employee(id):
    employee = Employee.query.get_or_404(id)

    if request.method == "POST":
        employee.employee_id = request.form["employee_id"].strip()
        employee.name = request.form["name"].strip()
        employee.email = request.form["email"].strip().lower()
        employee.phone = request.form["phone"].strip()
        employee.department = request.form["department"]
        employee.designation = request.form["designation"].strip()
        employee.salary = float(request.form["salary"])

        try:
            db.session.commit()
            return redirect(url_for("employee.home"))
        except Exception:
            db.session.rollback()
            return "Employee ID or Email already exists."

    return render_template(
        "edit_employee.html",
        employee=employee,
    )


@employee_bp.route("/delete/<int:id>")
@jwt_required()
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for("employee.home"))


@employee_bp.route("/api/employees", methods=["GET"])
@jwt_required()
def api_get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])


@employee_bp.route("/api/employees/<int:id>", methods=["GET"])
@jwt_required()
def api_get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())


@employee_bp.route("/api/employees", methods=["POST"])
@jwt_required()
def api_add_employee():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "employee_id",
        "name",
        "email",
        "phone",
        "department",
        "designation",
        "salary",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing fields: " + ", ".join(missing_fields),
        }), 400

    employee = Employee(
        employee_id=data["employee_id"].strip(),
        name=data["name"].strip(),
        email=data["email"].strip().lower(),
        phone=data["phone"].strip(),
        department=data["department"].strip(),
        designation=data["designation"].strip(),
        salary=float(data["salary"]),
    )

    try:
        db.session.add(employee)
        db.session.commit()
        return jsonify({
            "message": "Employee added successfully",
            "employee": employee.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Employee ID or Email already exists",
        }), 400


@employee_bp.route("/api/employees/<int:id>", methods=["PUT"])
@jwt_required()
def api_update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    employee.employee_id = data.get("employee_id", employee.employee_id)
    employee.name = data.get("name", employee.name)
    employee.email = data.get("email", employee.email)
    employee.phone = data.get("phone", employee.phone)
    employee.department = data.get("department", employee.department)
    employee.designation = data.get("designation", employee.designation)

    if "salary" in data:
        employee.salary = float(data["salary"])

    try:
        db.session.commit()
        return jsonify({
            "message": "Employee updated successfully",
            "employee": employee.to_dict(),
        })
    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Employee ID or Email already exists",
        }), 400


@employee_bp.route("/api/employees/<int:id>", methods=["DELETE"])
@jwt_required()
def api_delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({
        "message": "Employee deleted successfully",
    })
