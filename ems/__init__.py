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

    manager_password = bcrypt.generate_password_hash('manager').decode('utf-8')
    manager = User(username="manager", 
                       password=manager_password,
                       user_role="manager")

    db.session.add(super_admin)
    db.session.add(manager)
    db.session.commit()
    print("Super admin and manager added")

from ems import employee, department, auth, routes, bonus_cuts, manager, salary

app.register_blueprint(auth.bp)

api.add_resource(employee.EmployeeAPI, '/employees', '/employees/<int:employee_id>')

api.add_resource(department.DepartmentAPI, '/departments', '/departments/<int:dept_id>')

api.add_resource(manager.ManagerAPI, '/managers', '/managers/<int:user_id>')