from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.auth import *
from ems.schemas import *

class EmployeeAPI(Resource):
    @token_required_manager
    def post(self):
        if request.is_json:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            email = request.json['email']
            date_of_birth = request.json['date_of_birth']
            hourly_rate = request.json['hourly_rate']
            department_id = request.json['department_id']
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            date_of_birth = request.form['date_of_birth']
            hourly_rate = request.form['hourly_rate']
            department_id = request.form['department_id']

        employee = Employee.query.filter_by(email=email).first()

        if employee:
            abort(409, "Employee with that email address already exists")
        else:
            new_employee = Employee(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    date_of_birth=date_of_birth,
                                    hourly_rate=hourly_rate,
                                    department_id=department_id)
            
            db.session.add(new_employee)
            db.session.commit()

            result = employee_schema.dump(new_employee)
            response = jsonify(result)
            response.status_code = 201
            return response

    @token_required_manager
    def get(self, employee_id=None):
        if employee_id:
            employee = Employee.query.filter_by(id=employee_id).first()
            if employee:
                result = employee_schema.dump(employee)
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                abort(404, "No employee found")
        else:
            employee = Employee.query.all()
            if employee:
                result = employees_schema.dump(employee)
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                abort(404, "No employees found")

    @token_required_manager
    def put(self, employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee:
            if request.is_json:
                first_name = request.json['first_name']
                last_name = request.json['last_name']
                email = request.json['email']
                date_of_birth = request.json['date_of_birth']
                hourly_rate = request.json['hourly_rate']
                department_id = request.json['department_id']
            else:
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                date_of_birth = request.form['date_of_birth']
                hourly_rate = request.form['hourly_rate']
                department_id = request.form['department_id']
            
            employee.first_name=first_name
            employee.last_name=last_name
            employee.email=email
            employee.date_of_birth=date_of_birth
            employee.hourly_rate=hourly_rate
            employee.department_id=department_id

            db.session.commit()
            
            result = employee_schema.dump(employee)
            response = jsonify(result)
            response.status_code = 201
            return response
        
        else:
            abort(404, "No employee with that Id")

    @token_required_manager
    def delete(self, employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return jsonify(message="Employee successfully deleted"), 200
        else:
            abort(404, "No employee with that Id")