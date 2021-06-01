from datetime import datetime
from ems import db
from ems import login_manager
from flask_login import UserMixin
from flask_restful import fields

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    def __repr__(self):
        return f"Admin('{self.username}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.user_role}')"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    #date_of_birth = db.Column(db.DateTime, nullable=True, default=datetime.now)
    date_of_birth = db.Column(db.String, nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id') ,nullable=False)

    attendance = db.relationship('Attendance', backref='attend', lazy=True)
    bonus = db.relationship('BonusCuts', backref='bonus', lazy=True)
    salary = db.relationship('Salary', backref='salary', lazy=True)

    def __repr__(self):
        return f"Employee('{self.first_name}', '{self.last_name}', '{self.department_id}')"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_title = db.Column(db.String, nullable=False)
    no_of_employees = db.Column(db.Integer, nullable=False)
    employees = db.relationship('Employee', backref='works', lazy=True)

    def __repr__(self):
        return f"Department('{self.department_title}', '{self.no_of_employees}')"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Attendance('{self.employee_id}')"

class BonusCuts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    remark = db.Column(db.String, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"BonusCuts('{self.date}', '{self.amount}', '{self.employee_id}')"

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Salary('{self.date}', '{self.amount}', '{self.net}', '{self.employee_id}')"

admin_fields = {
    'id' : fields.Integer,
    'username' : fields.String,
    'password' : fields.String
}
user_fields = {
    'id' : fields.Integer,
    'user_role' : fields.String,
    'name' : fields.String,
    'password' : fields.String
}

attendance_fields = {
    'id' : fields.Integer,
    'employee_id' : fields.Integer
}

bonus_fields = {
    'id' : fields.Integer,
    'date' : fields.DateTime,
    'amount' : fields.Float,
    'remark' : fields.String,
    'employee_id' : fields.Integer
}

salary_fields = {
    'id' : fields.Integer,
    'date' : fields.DateTime,
    'amount' : fields.Float,
    'tax' : fields.Float,
    'net' : fields.Float,
    'employee_id' : fields.Integer
}

employee_fields = {
    'id' : fields.Integer,
    'first_name' : fields.String,
    'last_name' : fields.String,
    'date_of_birth' : fields.String,
    #'date_of_birth' : fields.DateTime,
    'hourly_rate' : fields.Float,
    'department_id' : fields.Integer,
    'attendance' : fields.Nested(attendance_fields),
    'bonus' : fields.Nested(bonus_fields),
    'salary' : fields.Nested(salary_fields)
}

department_fields = {
    'id' : fields.Integer,
    'department_title' : fields.String,
    'no_of_employees' : fields.Integer,
    'employees' : fields.Nested(employee_fields)
}