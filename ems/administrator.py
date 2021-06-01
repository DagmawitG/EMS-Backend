from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class AdministratorAPI(Resource):
    @marshal_with(user_fields)
    def post(self):
        if request.is_json:
            id = request.json['id']
            name = request.json['name']
            user_role = request.json['user_role']
            password = request.json['password']
        else:
            id = request.form['id']
            name = request.form['name']
            user_role = request.form['user_role']
            password = request.form['password']
            

        hrPerson = User.query.filter_by(name=name).first()

        if hrPerson:
            abort(409, message='HR person already exists')
        else:
            new_user = User(id=id,
                                    name=name,
                                    user_role=user_role,
                                    password=password
                                    )
            
            db.session.add(new_user)
            db.session.commit()

            return new_user, 201
    @marshal_with(user_fields)
    def delete(self, id):
        hrPerson = User.query.filter_by(id=id).first()
        if hrPerson:
            db.session.delete(hrPerson)
            db.session.commit()
            return jsonify(message="HR person successfully deleted"), 204
        else:
            abort(404, message="No HR person with that Id")
    @marshal_with(user_fields)
    def put(self, id):
        hrPerson = User.query.filter_by(id=id).first()

        if hrPerson:
            if request.is_json:
                name = request.json['name']
                user_role = request.json['user_role']
                password = request.json['password']
            else:
                name = request.json['name']
                user_role = request.json['user_role']
                password = request.json['password']

            hrPerson.name = name
            hrPerson.user_role = user_role
            hrPerson.password = password

            db.session.commit()
            return hrPerson, 200
        
        else:
            abort(404, message="No HR person with this Id")
    @marshal_with(user_fields)
    def get(self, id=None):
        if id:
            hrPerson = User.query.filter_by(id=id).first()
            if hrPerson:
                return hrPerson, 200
            else:
                abort(404, message="No HR person found")
        else:
            hrPerson = User.query.all()
            if hrPerson:
                return hrPerson, 200
            else:
                abort(404, message="No HR person found")
