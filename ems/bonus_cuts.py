from flask import request, jsonify
from flask_restful import Resource, abort
from ems.models import *
from ems.schemas import *
from ems.auth import *

class BonusCutsAPI(Resource):
    @token_required_manager
    def post(self):
        if request.is_json:
            employee_id = request.json['employee_id']
            date = request.json['date']
            amount = request.json['amount']
            remark = request.json['remark']
        else:
            employee_id = request.form['employee_id']
            date = request.form['date']
            amount = request.form['amount']
            remark = request.form['remark']

        bonus = BonusCuts.query.filter_by(employee_id=employee_id).first()

        if bonus:
            abort(409, "Bonus for this employee already added")
        else:
            new_bonuscut = BonusCuts(employee_id=employee_id,date=date, amount=amount,remark=remark)
                
            db.session.add(new_bonuscut)
            db.session.commit()

            result = bonus.dump(new_bonuscut)
            response = jsonify(result)
            response.status_code = 201
            return response

    @token_required_manager
    def get(self, bonus_id=None):
        if bonus_id:
            bonus = BonusCuts.query.filter_by(id=bonus_id).first()
            if bonus:
                result = department_schema.dump(bonus)
                response = jsonify(result)
                response.status_code = 201
                return response

            else:
                abort(404, "No Bonus/Cut found")
        else:
            bonus = BonusCuts.query.all()
            if bonus:
                result = bomus_schema.dump(bonus)
                response = jsonify(result)
                response.status_code = 201
                return response
            else:
                abort(404, "No Bonuses/Cuts found")

    @token_required_manager
    def put(self, bonus_id):
        bonus_cuts = BonusCuts.query.filter_by(id=bonus_id).first()
        if bonus_cuts:
            if request.is_json:
                bonus_id = request.json['id']
                bonus_date = request.json['date']
                bonus_amount = request.json['amount']
                bonus_remark = request.json['remark']
                bonuse_employee_id = request.json['employee_id']
            else:
                bonus_id = request.form['id']
                bonus_date = request.form['date']
                bonus_amount = request.form['amount']
                bonus_remark = request.form['remark']
                bonuse_employee_id = request.form['employee_id']

            bonus_cuts.id = bonus_id
            bonus_cuts.date = bonus_date
            bonus_cuts.amount = bonus_amount
            bonus_cuts.remark = bonus_remark
            bonus_cuts.employee_id = bonus_employee_id

            db.session.commit()

            result = bonus_schema.dump(bonus_cuts)
            response = jsonify(result)
            response.status_code = 201
            return response

        else:
            abort(404, "No bonus/cut with that Id")


    @token_required_manager
    def delete(self, bonus_id):
        bonus_cuts = BonusCuts.query.filter_by(id=bonus_id).first()
        if bonus_cuts:
            db.session.delete(bonus_cuts)
            db.session.commit()
            return jsonify(message="Bonus/Cut entry successfully deleted"), 200
        else:
            abort(404, "No bonus/cuts with that Id")