from flask import request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from ems.models import *

class AdminAPI(Resource): 
    #post for 1 and 2, password-token issue on db update/commit
    def post(self):
        if request.is_json:
            username = request.json['username']
            password = request.json['password']
            role = request.json['role']

        else:
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

        new_user = Admin.query.filter_by(username=username).first()

        if new_user:
            abort(409, message='User already exists')
        else:
            new_user = User(username=username, password=password, user_role=role)
            
            db.session.add(new_user)
            db.session.commit()

            return new_user, 201
    #3
    def delete(self, user_id = None):
        if not user_id: 
            if request.is_json: user_id = request.json['userId']
            else: user_id = request.form['userId']
    
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(message="User successfully deleted"), 204
        else:
            abort(404, message="No user with that Id")
    #4 update person
    def put(self):
        if request.is_json: user_id = request.json['user_id']
        else: user_id = request.form['user_id']

        user = User.query.filter_by(id=user_id).first()

        if user:
            if request.is_json:
                name = request.json['name']
                password = request.json['password']
                role = request.json['role']
            else:
                name = request.form['name']
                password = request.form['password']
                role = request.form['role']

            user.username = name
            user.password = password
            user.user_role = role

            db.session.commit()
            return user, 200
        
        else:
            abort(404, message="No user with that Id")
    #get for 5
    def get(self):
        users = Department.query.all()
        if users:
            return users, 200
        else:
            abort(404, "No users found")
