import sqlalchemy
import psycopg2
from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://ravik@localhost/oop_db')
Session = sessionmaker(bind = engine)
Base = declarative_base()
metadata = MetaData()
Table('employee', metadata, Column('id',Integer()),Column('name',String),extend_existing=True)
class Employee(Base):
	__tablename__ = 'employee'
	id = Column(Integer, primary_key = True)
	name = Column(String)
	def __init__(self,id,name):
		self.id = id
		self.name=name
# class Employee1:
# 	Table.extend_existing = True
# 	__tablename__ = 'employee'
# 	name = Column(String)
# 	def __init__(self,name):
# 		self.name = name


#metadata.create_all(engine)
emp = Employee(2,"ravi")
#emp1 = Employee(8,"ankur")
session = Session()
session.add(emp)
session.query(Employee).filter(Employee.id==emp.id).update({'name':"mahesh"})
#session.add(emp1)
# for emp in session.query(Employee).order_by(Employee.name).filter(Employee.id>=3):
# print emp.name
session.commit()
