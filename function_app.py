import azure.functions as func
import logging
from flask import Flask, Response,  jsonify, request 

flask_app = Flask(__name__) 

students = [
    {"id": 1, "name": "John", "course": "Physics"},
    {"id": 2, "name": "Sarah", "course": "Chemistry"},
    {"id": 3, "name": "Bob", "course": "English"},
    {"id": 4, "name": "Sebastian", "course": "French"},
    {"id": 5, "name": "Jill", "course": "History"},
]

app = func.WsgiFunctionApp(app=flask_app.wsgi_app, 
                           http_auth_level=func.AuthLevel.ANONYMOUS) 

@flask_app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"students": students})

@flask_app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student is not None:
        return jsonify({"student": student})
    else:
        return {"error": "student not found"}, 404

@flask_app.route('/students', methods=['POST'])
def create_student():
    new_student = request.get_json()
    students.append(new_student)
    return jsonify({"student": new_student}), 201

@flask_app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student is not None:
        updated_student = request.get_json()
        student.update(updated_student)
        return jsonify({"student": student})
    else:
        return {"error": "student not found"}, 404

@flask_app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return {"result": "student deleted"}