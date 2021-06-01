from flask import request, jsonify
from flask_restful import Api, Resource, abort, marshal_with
from ems.models import *
from ems.auth import *
from ems.resource_fields import *

class DepartmentAPI(Resource):
    @marshal_with(department_fields)
    @token_required_hr
    def post(self):
        if request.is_json:
            title = request.json['department_title']
            no_of_employees = request.json['no_of_employees']
        else:
            title = request.form['department_title']
            no_of_employees = request.form['no_of_employees']

        dept = Department.query.filter_by(department_title=title).first()

        if dept:
            abort(409, 'Department already exists')
        else:
            new_dept = Department(department_title=title,
                                  no_of_employees=no_of_employees)
            
            db.session.add(new_dept)
            db.session.commit()

            return new_dept, 201

    @marshal_with(department_fields)
    @token_required_hr
    def get(self, dept_id=None):
        if dept_id:
            dept = Department.query.filter_by(id=dept_id).first()
            if dept:
                return dept, 200
            else:
                abort(404, "No department found")
        else:
            dept = Department.query.all()
            if dept:
                return dept, 200
            else:
                abort(404, "No departments found")

    @marshal_with(department_fields)
    @token_required_hr
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
            abort(404, "No department with that Id")

    @marshal_with(department_fields)
    @token_required_hr
    def delete(self, dept_id):
        dept = Department.query.filter_by(id=dept_id).first()
        if dept:
            db.session.delete(dept)
            db.session.commit()
            return {'message': 'Department successfully deleted'}, 204
        else:
            abort(404, "No department with that Id")