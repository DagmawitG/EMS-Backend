from ems import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.user_role}')"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id') ,nullable=False)

    attendance = db.relationship('Attendance', backref='attend', lazy='True')
    bonus = db.relationship('Bonus', backref='bonus', lazy='True')
    salary = db.relationship('Salary', backref='salary', lazy='True')

    def __repr__(self):
        return f"Employee('{self.first_name}', '{self.last_name}', '{self.department_id}')"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_title = db.Column(db.String, nullable=False)
    no_of_employees = db.Column(db.Integer, nullable=False)
    employees = db.relationship('Employee', backref='works', lazy='True')

    def __repr__(self):
        return f"Department('{self.department_title}', '{self.no_of_employees}')"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Attendance('{self.employee_id}')"

class BonusCuts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    remark = db.Column(db.String, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Employee('{self.date}', '{self.amount}', '{self.employee_id}')"

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __repr__(self):
        return f"Employee('{self.date}', '{self.amount}', '{self.net}', '{self.employee_id}')"


