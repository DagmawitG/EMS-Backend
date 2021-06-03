from flask import Blueprint, request, jsonify, abort, make_response, session
from functools import wraps
from ems import app, db, bcrypt
from flask_login import login_user, current_user, logout_user
from ems.models import *
import jwt
import datetime

bp = Blueprint('auth', __name__)

def token_required_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            currentUser = User.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

        if not currentUser.user_role == "admin":
            return {'message' : 'You are not authorized'}

        return f(*args, **kwargs)

    return decorated

def token_required_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            currentUser = User.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

        if not currentUser.user_role == "manager":
            return {'message' : 'You are not authorized'}
            
        return f(*args, **kwargs)

    return decorated

@bp.route('/login', methods=['POST'])
def login():
    # if current_user.is_authenticated():
    #     return jsonify({'message': "Already logged in"})

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return abort(404, "Could not verify")

    try:
        user = User.query.filter_by(username = auth.username).first()
        if not user:
            return abort(404, "No user found")

        if bcrypt.check_password_hash(user.password, auth.password):
            if user.user_role == "admin":
                token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
                # login_user(user)
                session["type"] = user.user_role
                # return jsonify({'message': "admin login successful"})
                return jsonify({'token': token})
                
            elif user.user_role == "manager":
                token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
                # login_user(user)
                session["type"] = user.user_role
                # return jsonify({'message': "hr login successful"})
                return jsonify({'token': token})

        return jsonify(message="Invalid credentials")    
            
    except Exception as e:
        return jsonify({'message': str(e)})

    # if current_user.is_authenticated():
    #     return jsonify({'message': "Already logged in"})

    # if request.is_json:
    #     username = request.json['username']
    #     password = request.json['password']
    # else:
    #     username = request.form['username']
    #     password = request.form['password']

    # try:
    #     if username and password:
    #         user = User.query.filter_by(username = username).first()
    #         if user and bcrypt.check_password_hash(user.password, password):
    #             if user.user_role == "admin":
    #                 login_user(user)
    #                 return jsonify({'message': "admin login successful"})
    #             elif user.user_role == "hr":
    #                 login_user(user)
    #                 return jsonify({'message': "hr login successful"})
    #         else:
    #             abort(404, {'message': "Invalid login"})
    #     else:
    #         raise Exception("Login info is missing")

    # except Exception as e:
    #     return jsonify({'message': str(e)})

@bp.route('/logout', methods=['POST'])
def logout():
    # logout_user()
    session["type"] = ""
    return jsonify({'message': "Logged out successfully"})  
