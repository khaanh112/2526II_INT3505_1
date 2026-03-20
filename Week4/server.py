from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

students = [
	{"id": 1, "full_name": "Nguyen Van A", "email": "a.nguyen@example.com", "year": 1},
	{"id": 2, "full_name": "Tran Thi B", "email": "b.tran@example.com", "year": 2},
]


def validate_student_payload(payload, current_student_id=None):
	required_fields = ["full_name", "email", "year"]
	missing_fields = [field for field in required_fields if field not in payload]
	if missing_fields:
		return error_response(
			"VALIDATION_ERROR",
			f"Missing required field(s): {', '.join(missing_fields)}",
			400,
		)

	if not isinstance(payload["year"], int) or payload["year"] < 1 or payload["year"] > 4:
		return error_response("VALIDATION_ERROR", "year must be an integer between 1 and 4", 400)

	existing_student = next(
		(
			student
			for student in students
			if student["email"] == payload["email"] and student["id"] != current_student_id
		),
		None,
	)
	if existing_student:
		return error_response("DUPLICATE_EMAIL", "email already exists", 409)

	return None


def success_response(data, message="Success", status_code=200):
	return jsonify({"success": True, "data": data, "message": message}), status_code


def error_response(code, message, status_code):
	return jsonify({"success": False, "error": {"code": code, "message": message}}), status_code

@app.get("/")
def index():
	return success_response({"message": "Welcome to Khaanh's API"}, "API is working")

@app.get("/health")
def health_check():
	return success_response({"status": "ok"}, "Service is healthy")


@app.get("/students")
def get_students():
	year = request.args.get("year", type=int)
	result = students

	if year is not None:
		result = [student for student in students if student["year"] == year]

	return success_response(result)


@app.get("/students/<int:student_id>")
def get_student(student_id):
	student = next((item for item in students if item["id"] == student_id), None)
	if not student:
		return error_response("STUDENT_NOT_FOUND", "Student not found", 404)

	return success_response(student)


@app.post("/students")
def create_student():
	payload = request.get_json(silent=True)
	if not payload:
		return error_response("INVALID_BODY", "JSON body is required", 400)

	validation_error = validate_student_payload(payload)
	if validation_error:
		return validation_error

	new_student = {
		"id": (max([item["id"] for item in students]) + 1) if students else 1,
		"full_name": payload["full_name"],
		"email": payload["email"],
		"year": payload["year"],
	}
	students.append(new_student)
	return success_response(new_student, "Student created", 201)


@app.put("/students/<int:student_id>")
def update_student(student_id):
	student = next((item for item in students if item["id"] == student_id), None)
	if not student:
		return error_response("STUDENT_NOT_FOUND", "Student not found", 404)

	payload = request.get_json(silent=True)
	if not payload:
		return error_response("INVALID_BODY", "JSON body is required", 400)

	validation_error = validate_student_payload(payload, current_student_id=student_id)
	if validation_error:
		return validation_error

	student["full_name"] = payload["full_name"]
	student["email"] = payload["email"]
	student["year"] = payload["year"]

	return success_response(student, "Student updated", 200)


@app.delete("/students/<int:student_id>")
def delete_student(student_id):
	student = next((item for item in students if item["id"] == student_id), None)
	if not student:
		return error_response("STUDENT_NOT_FOUND", "Student not found", 404)

	students.remove(student)
	return success_response(None, "Student deleted", 200)


@app.get("/openapi.yaml")
def openapi_spec():
	spec_path = Path(__file__).with_name("openapi.yaml")
	return send_file(spec_path, mimetype="text/yaml")


swagger_ui = get_swaggerui_blueprint(
	"/docs",
	"/openapi.yaml",
	config={"app_name": "Week4 Flask API Demo"},
)
app.register_blueprint(swagger_ui, url_prefix="/docs")


@app.errorhandler(404)
def not_found(_error):
	return error_response("NOT_FOUND", "URL does not exist", 404)


@app.errorhandler(405)
def method_not_allowed(_error):
	return error_response("METHOD_NOT_ALLOWED", "HTTP method is not supported", 405)


if __name__ == "__main__":
	app.run(debug=True)
