import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

def Search3(curs,connection): #the sql query hasn't been built yet. Will get to that eventually, unless you guys there before me
	
	curs.execute("SELECT serial_no FROM vehicle")
	s3_col_vserial = curs.fetchall()	
	vrowlst = []	
	for vrow in s3_col_vserial:
		vrowlst.append(vrow[0].strip())

	serial_no = input("Enter vehicle serial number: ")
	while serial_no == "" or serial_no not in vrowlst:
		if serial_no not in vrowlst:
			serial_no = input("Vehicle already does not exist in database. Serial Number? or type 'exit' to main menu ").strip()
			if serial_no == "exit":
				return None##################
		elif serial_no == "":
			serial_no = input("Input cannot be blank. Serial Number? or type 'exit' to main menu ").strip()
			if serial_no == "exit":
				return None################
	
	
	curs.execute("select SERIAL_A SERIAL_NO, NUMBER_SALES, AVERAGE_PRICE, TOTAL_TICKETS from (SELECT v.serial_no SERIAL_A, count(distinct a.transaction_id) NUMBER_SALES, avg(a.price) AVERAGE_PRICE from (vehicle v left outer join auto_sale a on v.serial_no = a.vehicle_id) group by v.serial_no), (SELECT f.serial_no SERIAL_B, count(distinct t.ticket_no) TOTAL_TICKETS from (vehicle f left outer join ticket t on f.serial_no = t.vehicle_id) group by f.serial_no) where SERIAL_A = SERIAL_B and SERIAL_A = '" + serial_no + "'")

	print(" SERIAL_NO       , NUMBER_SALES, AVERAGE_PRICE, TOTAL_TICKETS")
	v_history = curs.fetchall()
	for v_history_row in v_history:
		print(v_history_row)
