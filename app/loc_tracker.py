import datetime
import copy
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, DateTime, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.types as types

engine = create_engine('postgresql://ravik@localhost/oop_db')
Session = sessionmaker(bind = engine)
Base = declarative_base()
metadata = MetaData()
session = Session()

Table("employee",metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String)
	)

Table("location",metadata,
	Column('id', Integer, primary_key = True),
	Column('building', String),
	Column('floor', String)
	)

Table("LogHistory",metadata,
	Column('emp_id', Integer, ForeignKey('employee.id'), primary_key=True),
	Column('login_time', DateTime, primary_key=True),
	Column('logout_time', DateTime),
	Column('loc_id', Integer, ForeignKey('location.id')),
	)

class Employee(Base):
	__tablename__ = "employee"
	id = Column(Integer, primary_key = True)
	name = Column(String)
	def __init__(self):
		self.id = 0
		self.name = ''
	def __init__(self,id,name):
		self.id = id
		self.name = name
	def is_valid(self):
		count = session.query(Employee).filter(Employee.id == self.id).count()
		if(count == 1):
			return True
		return False
	def print_current_location(self):
		for res in session.query(LogHistory).filter().filter(LogHistory.emp_id == self.id).filter(LogHistory.logout_time == None):
			if(res!=None):
				print "in compound"
				print res.loc_id
	def likely_position(self):
		x = session.query(LogHistory).filter(LogHistory.emp_id == self.emp_id).group_by(Location.loc_id).count().order_by(count()).one()
		print x
	def stay_time(self):
		session.query(LogHistory).filter(LogHistory.emp_id == self.emp_id)
class Location(Base):
	__tablename__ = "location"
	id = Column(Integer, primary_key = True)
	building = Column(String)
	floor = Column(String)
	def __init__(self):
		self.building = ''
		self.floor = ''
	def __init__(self,building,floor):
		self.building = building
		self.floor = floor

class LogHistory(Base):
	__tablename__ = "LogHistory"
	emp_id = Column(Integer, primary_key = True)
	login_time = Column(DateTime, primary_key = True)
	logout_time = Column(DateTime)
	loc_id = Column(Integer)
	def __init__(self):
		pass
	def __init__(self, emp, loc):
		self.emp_logging_obj = emp
		self.emp_id = emp.id
		building = loc.building
		floor = loc.floor
		for locs in session.query(Location).filter(Location.building == building).filter(Location.floor == floor):
			self.loc_id = locs.id
		self.login_time = datetime.datetime.now()
		self.logout_time = None
	def login(self):
		if(self.emp_logging_obj.is_valid() == True):
			self.add_to_db();
	def logout(self):
		self.logout_time = datetime.datetime.now()
		session.query(LogHistory).filter(LogHistory.emp_id == self.emp_id).filter(LogHistory.login_time == self.login_time).update({LogHistory.logout_time : self.logout_time})

	def add_to_db(self):
		session.add(self)
		session.commit()
metadata.create_all(engine)