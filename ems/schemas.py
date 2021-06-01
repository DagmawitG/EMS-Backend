from ems import ma

class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'username', 'password', 'user_role')

class EmployeeSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'hourly_rate', 'department_id', 'attendance', 'bonus', 'salary')

class DepartmentSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'department_title', 'no_of_employees', 'employees')

class AttendanceSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'work_time', 'employee_id')

class BonusSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'date', 'amount', 'remark', 'employee_id')

class SalarySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'date', 'amount', 'tax', 'net', 'employee_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

department_schema = EmployeeSchema()
departments_schema = EmployeeSchema(many=True)

attendance_schema = AttendanceSchema()
attendances_schema = AttendanceSchema(many=True)

bonus_schema = BonusSchema()
bonuss_schema = BonusSchema(many=True)

salary_schema = SalarySchema()
salaries_schema = SalarySchema(many=True)