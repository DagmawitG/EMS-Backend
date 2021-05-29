from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class EmployeeAPI(Resource):
    @marshal_with(employee_fields)
    def post(self):
        first_name = request.form['first_name']
        employee = Employee.query.filter_by(first_name=first_name).first()

        if employee:
            abort(409, message='Employee already exists')
        else:
            last_name = request.form['last_name']
            date_of_birth = request.form['date_of_birth']
            hourly_rate = request.form['hourly_rate']
            department_id = request.form['department_id']

            new_employee = Employee(first_name=first_name,
                                    last_name=last_name,
                                    date_of_birth=date_of_birth,
                                    hourly_rate=hourly_rate,
                                    department_id=department_id)
            
            db.session.add(new_employee)
            db.session.commit()

            return new_employee, 201

    @marshal_with(employee_fields)
    def get(self, employee_id=None):
        if employee_id:
            employee = Employee.query.filter_by(id=employee_id).first()
            if employee:
                return employee, 200
            else:
                abort(404, message="No employee found")
        else:
            employee = Employee.query.all()
            if employee:
                return employee, 200
            else:
                abort(404, message="No employees found")

    @marshal_with(employee_fields)
    def put(self, employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            date_of_birth = request.form['date_of_birth']
            hourly_rate = request.form['hourly_rate']
            department_id = request.form['department_id']
            
            employee.first_name=first_name
            employee.last_name=last_name
            employee.date_of_birth=date_of_birth
            employee.hourly_rate=hourly_rate
            employee.department_id=department_id

            db.session.commit()
            return employee, 200
        
        else:
            abort(404, message="No employee with that Id")

    @marshal_with(employee_fields)
    def delete(self, employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return jsonify(message="Employee successfully deleted"), 204
        else:
            abort(404, message="No employee with that Id")