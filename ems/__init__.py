from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SECRET_KEY'] = 'oursupersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)
ma = Marshmallow(app)

from ems.models import User

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("DB Created")

@app.cli.command('db_drop')
def db_create():
    db.drop_all()
    print("DB Dropped")

@app.cli.command('db_seed')
def db_seed():
    admin_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    super_admin = User(username="admin", 
                       password=admin_password,
                       user_role="admin")

    hr_password = bcrypt.generate_password_hash('hr').decode('utf-8')
    hr = User(username="hr", 
                       password=hr_password,
                       user_role="hr")

    db.session.add(super_admin)
    db.session.add(hr)
    db.session.commit()
    print("Super admin and hr added")

from ems import employee, department, auth, routes

app.register_blueprint(auth.bp)

api.add_resource(employee.EmployeeAPI, '/employees', '/employees/<int:employee_id>')
api.add_resource(department.DepartmentAPI, '/departments', '/departments/<int:dept_id>')