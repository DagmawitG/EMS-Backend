from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.schemas import *
from ems.auth import *



def calculate_salary(employee_id):
    return getBonusSum(employee_id) + (getWorkHourSum(employee_id)*getHourlyRate(employee_id))
def getTax(employee_id):
    return .15 * getHourlyRate(employee_id) * getWorkHourSum(employee_id)
def getBonusSum(employee_id):
    bonus_and_cuts = 0
    bnc = BonusCuts.query.filter_by(employee_id=sal_employee_id)
    if bnc:
        bnc = bnc.all()
        for bonus in bnc:
            bonus_and_cuts+=bonus.amount
            BonusCutsAPI.delete(bonus.id)
    return bonus_and_cuts
def getWorkHourSum(employee_id):
    hours = 0
    h = Attendance.query.filter_by(employee_id=sal_employee_id)
    h = h.all()
    for hour_entry in h:
        hours+=h.work_time
        AttendanceAPI.delete(hour_entry.id)
    return hours
def getHourlyRate(employee_id):
    hourly_rate = Employee.query.filter_by(id=sal_employee_id).first().hourly_rate


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
    @token_required_manager
    def post(self):
        salary_date = None
        if request.is_json:
            salary_id = request.json['id']
            if request.json['date']: salary_date = request.json['date']
            salary_amount = request.json['amount']
            salary_tax = request.json['tax']
            salary_net = request.json['net']
            salary_employee_id = request.json['employee_id']
        else:
            salary_id = request.form['id']
            if request.form['date']: salary_date = request.form['date']
            salary_amount = request.form['amount']
            salary_tax = request.form['tax']
            salary_net = request.form['net']
            salary_employee_id = request.form['employee_id']

        salary = Salary.query.filter_by(id=salary_id).first()

        if salary:
            abort(409, 'Salary already exists')
        else:
            if salary_date:
                new_sal = Salary(date = salary_date, amount = salary_amount, tax = salary_tax, net = salary_net, employee_id = salary_employee_id)
            else:
                new_sal = Salary(amount = salary_amount, tax = salary_tax, net = salary_net, employee_id = salary_employee_id)
            db.session.add(new_sal)
            db.session.commit()

            result = salary_schema.dump(new_sal)
            response = jsonify(result)
            response.status_code = 200
            return response

    @token_required_manager
    def get(self, sal_id):
        sal_tbl = Salary.query.filter_by(id=sal_id).first()
        if sal_tbl:
            if request.is_json:
                sal_date = request.json['date']
                sal_employee_id = request.json['employee_id']
            else:
                sal_date = request.form['date']
                sal_employee_id = request.form['employee_id']
            return_json = {}
            return_json["date"] = sal_date
            return_json["tax"] = getTax(employee_id)
            return_json["amount"] = calculate_salary(employee_id)
            return_json["employee_id"] = return_json["amount"]-return_json["tax"]
            return_json["employee_id"] = sal_employee_id

            # db.session.commit()

            # result = salary_schema.dump(sal_tbl)
            # response = jsonify(result)
            # response.status_code = 201
            return return_json

        else:
            abort(404, "No department with that Id")

    @token_required_manager
    def delete(self, sal_id):
        sal = Salary.query.filter_by(id=sal_id).first()
        if sal:
            db.session.delete(sal)
            db.session.commit()
            return jsonify(message="Salary successfully deleted"), 200
        else:
            abort(404, "No department with that Id")
