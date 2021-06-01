from flask_restful import fields

user_fields = {
    'id' : fields.Integer,
    'username' : fields.String,
    'password' : fields.String,
    'user_role' : fields.String
}

attendance_fields = {
    'id' : fields.Integer,
    'employee_id' : fields.Integer,
    'work_time': fields.Integer
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
    'email' : fields.String,
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