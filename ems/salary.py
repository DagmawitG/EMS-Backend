from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class SalaryAPI(Resource):
    #Gets salary (16)
    @marshal_with(salary_fields)
    def get(self, employee_id = None, date = None):
        if employee_id:
            salaries = Salary.query.filter_by(employee_id=employee_id)
            if salaries:
                return salaries, 200
            else:
                abort(404, message=f"No salaries found for employee id : {employee_id}")
        elif date:
            salaries = Salary.query.filter_by(date=date)
            if salaries:
                return salaries, 200
            else:
                abort(404, message=f"No salaries found for date : {date}")

        else:
            salaries = Salary.query.all()
            if salaries:
                return salaries, 200
            else:
                abort(404, message="No salaries found")
