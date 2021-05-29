from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SECRET_KEY'] = 'oursupersecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("DB Created")

@app.cli.command('db_drop')
def db_create():
    db.drop_all()
    print("DB Dropped")

from ems import employee

api.add_resource(employee.EmployeeAPI, '/employees', '/employees/<int:employee_id>')