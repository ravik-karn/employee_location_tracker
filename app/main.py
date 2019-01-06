from loc_tracker import *
import sqlalchemy.sql.expression
def data_handler(id, building, floor):
	name = 'ravi'
	emp = Employee(id, name)
	loc = Location(building, floor)
	login_obj = LogHistory(emp,loc)
	login_obj.login()
	login_obj.print_current_location()
def logout_handler(id):
	pass
def  emp_loc_exact(id):
	pass
def  emp_loc_prob(id):
	pass
def  emp_duration(id):
	pass
def floor_map():
	pass