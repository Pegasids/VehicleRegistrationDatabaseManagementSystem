import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

def Search2(curs,connection):

	curs.execute("SELECT sin FROM people")
	all_sin = curs.fetchall()	
	sin_lst = []	
	for sin in all_sin:
		sin_lst.append(sin[0].strip())

	curs.execute("SELECT licence_no FROM drive_licence")
	all_dln = curs.fetchall()	
	dln_lst = []	
	for dln in all_dln:
		dln_lst.append(dln[0].strip())



	sin_or_dln = input("Do you want to use SIN or DRIVER_LICENCE_NO as an input: (s/d) ").strip()
	while sin_or_dln not in ['s','d']:
		sin_or_dln = input("Invalid Input. Do you want to use SIN or DRIVER_LICENCE_NO as an input: (s/d) ").strip()

	if sin_or_dln == "s":
		sin = input("SIN? ").strip()
		while sin not in sin_lst:
			sin = input("SIN doesn't exist in database! Enter a valid SIN or type 'exit' to main menu ").strip()
			if sin == "exit":
				return None
		
				
		curs.execute("SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, TO_CHAR(t.vdate, 'YYYY-MM-DD'), t.place, t.descriptions FROM ticket t where t.violator_no = '" + sin + "'")

		all_vr = curs.fetchall()
		if all_vr == []:
			print("This person dosn't have any violation record.")
		else:

			for vr in all_vr:
				print("Ticket Number: ", vr[0])
				print("Violator Number: ", vr[1])
				print("Vehicle Number: ", vr[2])
				print("Office Number: ", vr[3])
				print("Violtion Type: ", vr[4])
				print("Violaion Date: ", vr[5])
				print("Place: ", vr[6])
				print("Descriptios: ", vr[7])
				print("")

		
	elif sin_or_dln == "d":
		dln = input("Driver Licence Number? ").strip()
		while dln not in dln_lst:
			dln = input("DLN doesn't exist in database! Enter a valid Driver Licence Number or type 'exit' to main menu ").strip()
			if dln == "exit":
				return None

		
		curs.execute("select d.licence_no, t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, TO_CHAR(t.vdate, 'YYYY-MM-DD'), t.place, t.descriptions from ticket t, drive_licence d where d.sin = t.violator_no and d.licence_no = '" + dln + "'")


		all_vr = curs.fetchall()
		if all_vr == []:
			print("This person dosn't have any violation record.")
		else:

			for vr in all_vr:

				print("Licence Number: ", vr[0])
				print("Ticket Number: ", vr[1])
				print("Violator Number: ", vr[2])
				print("Vehicle Number: ", vr[3])
				print("Office Number: ", vr[4])
				print("Violation Type: ", vr[5])
				print("Violation Date: ", vr[6])
				print("Place: ", vr[7])
				print("Descriptions: ", vr[8])
				print("")
	
