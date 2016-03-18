import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

# List all violation records received by a person if the drive licence_no or sin of a person  is entered.
def Search2(curs,connection):

	curs.execute("SELECT sin FROM people")		# Add all the sin from people to a list.
	all_sin = curs.fetchall()	
	sin_lst = []	
	for sin in all_sin:
		sin_lst.append(sin[0].strip())

	curs.execute("SELECT licence_no FROM drive_licence")	# Add all the licence_no from drive_licence to a list.
	all_dln = curs.fetchall()	
	dln_lst = []	
	for dln in all_dln:
		dln_lst.append(dln[0].strip())


	# Ask user to choose from either to enter a SIN or a Licence_no.
	sin_or_dln = input("Do you want to use SIN or DRIVER_LICENCE_NO as an input: (s/d) ").strip()
	while sin_or_dln not in ['s','d']:
		sin_or_dln = input("Invalid Input. Do you want to use SIN or DRIVER_LICENCE_NO as an input: (s/d) ").strip()

	# If user wants to enter SIN.
	if sin_or_dln == "s":
		sin = input("SIN? ").strip()	# Ask for SIN.
		while sin not in sin_lst:	# Raise error if SIN doesnt exist.
			sin = input("SIN doesn't exist in database! Enter a valid SIN or type 'exit' to main menu ").strip()
			if sin == "exit":
				return None
		
		# Run the query.
		curs.execute("SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, TO_CHAR(t.vdate, 'YYYY-MM-DD'), t.place, t.descriptions FROM ticket t where t.violator_no = '" + sin + "'")
		# Print all the outputs.
		all_vr = curs.fetchall()
		if all_vr == []:	# If SIN exist but doesn't have any violation record , do the following.
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

	# If user wants to enter a Licence_no.
	elif sin_or_dln == "d":
		dln = input("Driver Licence Number? ").strip()		# Ask for Licence_no.
		while dln not in dln_lst:				# Raise error if Licence_no doesnt exist
			dln = input("DLN doesn't exist in database! Enter a valid Driver Licence Number or type 'exit' to main menu ").strip()
			if dln == "exit":
				return None

		# Run the query.
		curs.execute("select d.licence_no, t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, TO_CHAR(t.vdate, 'YYYY-MM-DD'), t.place, t.descriptions from ticket t, drive_licence d where d.sin = t.violator_no and d.licence_no = '" + dln + "'")

		# Print all the outputs.
		all_vr = curs.fetchall()
		if all_vr == []:	# If Licence_no exist but doesn't have any violation record , do the following.
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
	
