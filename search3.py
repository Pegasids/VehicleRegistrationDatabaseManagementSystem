import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

# Print out the vehicle_history, including the number of times that a vehicle has been changed hand, the average price, and the number of violations it has been involved by entering the vehicle's serial number.
def Search3(curs,connection):
	
	curs.execute("SELECT serial_no FROM vehicle")			# Add all the serial_no from vehicle into a list to check for any invalid serial_no.
	s3_col_vserial = curs.fetchall()	
	vrowlst = []	
	for vrow in s3_col_vserial:
		vrowlst.append(vrow[0].strip())

	serial_no = input("Enter vehicle serial number: ").strip()	# Ask user to enter a serial_no.
	while serial_no == "" or serial_no not in vrowlst:		# Raise error if user enter blank or non-existing serial_no.
		if serial_no not in vrowlst:
			serial_no = input("Vehicle already does not exist in database. Serial Number? or type 'exit' to main menu ").strip()
			if serial_no == "exit":
				return None
		elif serial_no == "":
			serial_no = input("Input cannot be blank. Serial Number? or type 'exit' to main menu ").strip()
			if serial_no == "exit":
				return None
	
	# if serial_no is valid, do the following query.
	curs.execute("select SERIAL_A SERIAL_NO, NUMBER_SALES, AVERAGE_PRICE, TOTAL_TICKETS from (SELECT v.serial_no SERIAL_A, count(distinct a.transaction_id) NUMBER_SALES, avg(a.price) AVERAGE_PRICE from (vehicle v left outer join auto_sale a on v.serial_no = a.vehicle_id) group by v.serial_no), (SELECT f.serial_no SERIAL_B, count(distinct t.ticket_no) TOTAL_TICKETS from (vehicle f left outer join ticket t on f.serial_no = t.vehicle_id) group by f.serial_no) where SERIAL_A = SERIAL_B and SERIAL_A = '" + serial_no + "'")
	
	# Print out all the output.
	v_history = curs.fetchall()
	for v_history_row in v_history:
		print("Serial Number: ", v_history_row[0])
		print("Number of sales: ", v_history_row[1])
		print("Average price: ", v_history_row[2])
		print("Total tickets: ", v_history_row[3])
