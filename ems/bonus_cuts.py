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