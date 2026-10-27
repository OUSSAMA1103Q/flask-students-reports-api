from flask import Flask, request

app = Flask(__name__)

students = [
    {
        "id": 1,
        "name": "John",
        "lastname": "Doe",
        "report": [
            {
                "title": "first work",
                "type": "mini senior project"
            }
        ]
    }
]


def find_student(student_id):
    return next((s for s in students if s["id"] == student_id), None)


@app.get("/student")
def get_students():
    return {"students": students}


@app.get("/student/<int:student_id>")
def get_student(student_id):
    student = find_student(student_id)
    if not student:
        return {"message": "student not found"}, 404
    return {"student": student}, 200


@app.post("/student")
def add_student():
    new_student = request.get_json()
    students.append(new_student)
    return {"message": "student added successfully", "student": new_student}, 201


@app.get("/student/<int:student_id>/report")
def get_student_reports(student_id):
    student = find_student(student_id)
    if not student:
        return {"message": "student not found"}, 404
    return {"reports": student["report"]}, 200


@app.post("/student/<int:student_id>/report")
def add_report(student_id):
    student = find_student(student_id)
    if not student:
        return {"message": "student not found"}, 404

    request_data = request.get_json()
    new_report = {
        "title": request_data.get("title"),
        "type": request_data.get("type")
    }
    student["report"].append(new_report)
    return {"message": "report added successfully", "report": new_report}, 201


@app.get("/student/<int:student_id>/report/<int:report_id>")
def get_student_report(student_id, report_id):
    student = find_student(student_id)
    if not student:
        return {"message": "student not found"}, 404

    if report_id < 0 or report_id >= len(student["report"]):
        return {"message": "report not found"}, 404

    report = student["report"][report_id]
    return {"report": report}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
