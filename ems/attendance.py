from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.schemas import *
from ems.auth import *

class AttendanceAPI(Resource):
    @token_required_manager
    def post(self):
        if request.is_json:
            employee_id = request.json['employee_id']
            work_time = request.json["work_time"]
        else:
            employee_id = request.form['employee_id']
            work_time = request.form["work_time"]

        new_attendance = Attendance(work_time = work_time, employee_id=employee_id)
            
        db.session.add(new_attendance)
        db.session.commit()

        result = attendance_schema.dump(new_attendance)
        response = jsonify(result)
        response.status_code = 201
        return response
    @token_required_manager
    def get(self, attendance_id=None):
        if attendance_id:
            attendance = Attendance.query.filter_by(id=attendance_id).first()
            if attendance:
                result = attendance_schema.dump(attendance)
                response = jsonify(result)
                response.status_code = 201
                return response
            else:
                abort(404, "No attendnace record found")
        else:
            attendance = Attendance.query.all()
            if attendance:
                result = attendances_schema.dump(attendance)
                response = jsonify(result)
                response.status_code = 201
                return response
            else:
                abort(404, "No attendance records found")

    @token_required_manager
    def put(self, attendance_id=None):
        if not attendance_id: abort(400, "Attendance ID required")
        attendance = Attendance.query.filter_by(id=attendance_id).first()
        if attendance:
            if request.is_json:
                employee_id = request.json['employee_id']
                work_time = request.json['work_time']
            else:
                employee_id = request.form['employee_id']
                work_time = request.form['work_time']

            attendance.id = attendance_id
            attendance.employee_id = employee_id
            attendance.work_time = work_time

            db.session.commit()

            result = attendance_schema.dump(attendance)
            response = jsonify(result)
            response.status_code = 201
            return response
        else:
            abort(404, "No department with that Id")
        
    @token_required_manager
    def delete(self, attendance_id = None):
        if not attendance_id: abort(400, "Attendance ID required")
        attendance = Attendance.query.filter_by(id=attendance_id).first()
        if attendance:
            db.session.delete(attendance)
            db.session.commit()
            return jsonify(message="Attendance Entry successfully deleted"), 200
        else:
            abort(404, "No attendace entry with that Id")