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