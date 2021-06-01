from flask import request, jsonify
from flask_restful import Resource, abort
from ems import bcrypt
from ems.models import *
from ems.schemas import *

class ManagerAPI(Resource):
    def post(self):
        if request.is_json:
            username = request.json['username']
            password = request.json['password']
            user_role = request.json['role']
        else:
            username = request.form['username']
            password = request.form['password']
            user_role = request.form['role']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_manager = User.query.filter_by(username=username).first()

        if new_manager:
            abort(409, message='User already exists')
        else:
            new_manager = User(username=username, password=hashed_password, user_role=user_role)
            
            db.session.add(new_manager)
            db.session.commit()

            result = user_schema.dump(new_manager)
            response = jsonify(result)
            response.status_code = 201
            return response

    def get(self, user_id=None):
        if user_id:
            manager = User.query.filter_by(id=user_id).first()
            if manager:
                result = user_schema.dump(manager)
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                abort(404, "No manager with that Id found")

        else:
            manager = User.query.all()
            if manager:
                result = users_schema.dump(manager)
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                abort(404, "No users found")

    def put(self, user_id):
        manager = User.query.filter_by(id=user_id).first()
        if manager:
            if request.is_json:
                name = request.json['name']
                password = request.json['password']
                user_role = request.json['user_role']
            else:
                name = request.form['name']
                password = request.form['password']
                user_role = request.form['role']

            manager.username = name
            manager.password = password
            manager.user_role = user_role

            db.session.commit()
            
            result = user_schema.dump(manager)
            response = jsonify(result)
            response.status_code = 200
            return response

        else:
            abort(404, message="No user with that Id")

    def delete(self, user_id):
        manager = User.query.filter_by(id=user_id).first()
        if manager:
            db.session.delete(manager)
            db.session.commit()
            return jsonify(message="Manager successfully deleted"), 200
        else:
            abort(404, message="No manager with that Id")