from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.schemas import *
from ems.auth import *

class SalaryAPI(Resource):
    @token_required_manager
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
