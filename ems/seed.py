import random
import datetime
from ems.models import User, Department, Employee
from ems import db, app
import string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def get_random_date(y1, y2):
    year = random.randint(y1, y2)
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')
    except ValueError:
        get_random_date(year)

@app.cli.command('db_add_department')
def db_add_department():
  n=3
  for i in range(n):
    department = Department(department_title = randomword(7), no_of_employees = random.randint(50,100))
    db.session.add(department)
    db.session.commit()
  print("the departments are getting stronger has commenced")

@app.cli.command('db_employee_spam')
def db_employee_spam():
  n=10
  department_ids = [r.id for r in db.session.query(Department.c.id).distinct()]
  for i in range(n):
    d_o_b = get_random_date(1960, 2000).strftime("%d/%m/%Y")
    hourly = random.randint(7,25)
    employee = Employee(first_name = randomword(10), last_name = randomword(10), email = randomword(10), date_of_birth=d_o_b, hourly_rate=hourly, department_id=department_ids[random.randint(0,len(department_ids))])
    db.session.add(employee)
    db.session.commit()
  print("emplyee spam has commenced")