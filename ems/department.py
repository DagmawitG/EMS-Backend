from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.auth import *
from ems.schemas import *

class DepartmentAPI(Resource):
    @token_required_manager
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

            result = department_schema.dump(new_dept)
            response = jsonify(result)
            response.status_code = 200
            return response

    @token_required_manager
    def get(self, dept_id=None):
        if dept_id:
            dept = Department.query.filter_by(id=dept_id).first()
            if dept:
                result = department_schema.dump(dept)
                response = jsonify(result)
                response.status_code = 201
                return response

            else:
                abort(404, "No department found")
        else:
            dept = Department.query.all()
            if dept:
                result = departments_schema.dump(dept)
                response = jsonify(result)
                response.status_code = 201
                return response
            else:
                abort(404, "No departments found")

    @token_required_manager
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

            result = department_schema.dump(dept)
            response = jsonify(result)
            response.status_code = 201
            return response

        else:
            abort(404, "No department with that Id")

    @token_required_manager
    def delete(self, dept_id):
        dept = Department.query.filter_by(id=dept_id).first()
        if dept:
            db.session.delete(dept)
            db.session.commit()
            return jsonify(message="Department successfully deleted"), 200
        else:
            abort(404, "No department with that Id")