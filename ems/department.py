from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class DepartmentAPI(Resource):
    @marshal_with(department_fields)
    def post(self):
        if request.is_json:
            title = request.json['department_title']
            no_of_employees = request.json['no_of_employees']
        else:
            title = request.form['department_title']
            no_of_employees = request.form['no_of_employees']

        dept = Department.query.filter_by(department_title=title).first()

        if dept:
            abort(409, message='Department already exists')
        else:
            new_dept = Department(department_title=title,
                                  no_of_employees=no_of_employees)
            
            db.session.add(new_dept)
            db.session.commit()

            return new_dept, 201

    @marshal_with(department_fields)
    def get(self, dept_id=None):
        if dept_id:
            dept = Department.query.filter_by(id=dept_id).first()
            if dept:
                return dept, 200
            else:
                abort(404, message="No department found")
        else:
            dept = Department.query.all()
            if dept:
                return dept, 200
            else:
                abort(404, message="No departments found")

    @marshal_with(department_fields)
    def put(self, dept_id):
        dept = Department.query.filter_by(id=dept_id).first()

        if dept:
            if request.is_json:
                title = request.json['department_title']
                no_of_employees = request.json['no_of_employees']
            else:
                title = request.form['department_title']
                no_of_employees = request.form['no_of_employees']

            dept.department_title = title
            dept.no_of_employees = no_of_employees

            db.session.commit()
            return dept, 200
        
        else:
            abort(404, message="No department with that Id")

    @marshal_with(department_fields)
    def delete(self, dept_id):
        dept = Department.query.filter_by(id=dept_id).first()
        if dept:
            db.session.delete(dept)
            db.session.commit()
            return jsonify(message="Department successfully deleted"), 204
        else:
            abort(404, message="No department with that Id")