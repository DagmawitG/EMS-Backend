from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class AttendanceAPI(Resource):
    #14 Adding attendance entry
    @marshal_with(attendance_fields)
    def post(self, employee_id = None):
        if request.is_json:
            work_time = request.json["work_time"]
            if not employee_id: employee_id = request.json['employee_id']
        else:
            work_time = request.form["work_time"]
            if not employee_id: employee_id = request.form['employee_id']

        new_attendance = Attendance(work_time = work_time, employee_id=employee_id)
            
        db.session.add(new_attendance)
        db.session.commit()

        return new_attendance, 201
