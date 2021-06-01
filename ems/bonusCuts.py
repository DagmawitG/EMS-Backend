from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class BonusCutsAPI(Resource):
    #Adding bonus/cuts (15)
    @marshal_with(bonus_fields)
    def post(self, employee_id = None):
        if request.is_json:
            if not employee_id: employee_id = request.json['employee_id']
            date = request.json['date']
            amount = request.json['amount']
            remark = request.json['remark']
        else:
            if not employee_id: employee_id = request.form['employee_id']
            date = request.form['date']
            amount = request.form['amount']
            remark = request.form['remark']

        new_bonuscut = BonusCuts(employee_id=employee_id,date=date, amount=amount,remark=remark)
            
        db.session.add(new_bonuscut)
        db.session.commit()

        return new_bonuscut, 201
