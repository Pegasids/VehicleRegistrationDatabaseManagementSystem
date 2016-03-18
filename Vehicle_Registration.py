# Avery Tan, Canopus Tong, Nathan Nguyen
#Project 1 CMPUT291



import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

def nvr_getdata(vtrows, vrows, sinrows):	# get data from user input and generate data in correct format

#-------Serial Number-----------------------------------------------------------------------------------------------------------
	vrowlst = []		# Add all the serial_no in a list.
	for vrow in vrows:
		vrowlst.append(vrow[0].strip())

	print("Vehicle Information")				
	serial_no = input("Serial Number? ").strip()          	# Ask for serial_no.
	while serial_no == "" or serial_no in vrowlst:		# if serial_no is blank or isn't unique, raise error.
		if serial_no in vrowlst:
			serial_no = input("Vehicle already exists in database. Serial Number? or type 'exit' to main menu ").strip()
			if serial_no == "exit":
				return None, None, None, None, None#========================================
		elif serial_no == "":
			serial_no = input("Input cannot be blank. Serial Number? or type 'exit' to main menu ").strip()
			if serial_no == "exit":
				return None, None, None, None, None#=========================================

#-------Maker-----------------------------------------------------------------------------------------------------------
	maker = input("Maker? ").strip()
	if maker == "": maker = None

#-------Model-----------------------------------------------------------------------------------------------------------
	model = input("Model? ").strip()
	if model == "": model = None

#-------Year-----------------------------------------------------------------------------------------------------------
	year = input("Year? ").strip()
	while not year.isdigit():
		if year == "": 
			year = None
			break
		year = input("Invalid input. Year? ").strip()
		if year == "": 
			year = None
			break
	if year != None: int(year)

#-------Color-----------------------------------------------------------------------------------------------------------
	color = input("Color? ").strip()
	if color == "": color = None

#-------List vehicle_type table-----------------------------------------------------------------------------------------------------------
	print("")
	print("(Type ID) (Type Name)")
	type_id_lst = []
	for vtrow in vtrows:
		type_id_lst.append(str(vtrow[0]))
		print(vtrow[0],". ",vtrow[1], sep='')

#-------Type ID-----------------------------------------------------------------------------------------------------------	
	type_id = input("Type ID? ").strip()				
	while not type_id.isdigit() or type_id not in type_id_lst:	# Raise error if type_id doesn't exist.
			type_id = input("Invalid input. Type ID? or type 'exit to main menu ").strip()
			if type_id == "exit":
				return None, None, None, None, None
	type_id = int(type_id)

#-------Number of Owner-----------------------------------------------------------------------------------------------------------
	number_of_owner = input("Number of owner? ").strip()
	while not number_of_owner.isdigit():
			number_of_owner = input("Invalid input. Number of owner? ").strip()
	number_of_owner = int(number_of_owner)

#-------Enter Vehicle Infos-----------------------------------------------------------------------------------------------------------	
	oid = []; ipo = [];  new_people2d = [];	# oid for owner data; ipo for IS_Primary data; new_people2d for new SIN data;
	for i in range (number_of_owner):			
		print("")

#---------------Owner ID---------------------------------------------------------------------------------------------------
		sin_rowlst = []; new_sin = [];
		for sin in sinrows:
			sin_rowlst.append(sin[0].strip())

		print("Owner", i + 1, "Information")
		owner_id = input("Owner ID? ").strip()			# has to be unique and references people
		while owner_id in oid or owner_id not in sin_rowlst:
			if owner_id == "":
				owner_id = input("Owner ID cannnot be blank. Owner ID? or type 'exit' to main menu ").strip()
				if owner_id == "exit":  
					return None, None, None, None, None
			elif owner_id in oid:
				owner_id = input("This Owner ID had already been entered. Owner ID? or type 'exit' to main menu ").strip()
				if owner_id == "exit": 
					return None, None, None, None, None
			elif owner_id not in sin_rowlst:	# Ask user if they want to add this non-existing SIN to database.
				truth_val = input("Owner ID doesn't exist. Do you want to add this new SIN to DataBase?(y/n) or type 'exit' to main menu ").strip()
				if truth_val == "exit": 
					return None, None, None, None, None
				while truth_val not in ['y','n','Y','N']:
					truth_val = input("Invalid input. Do you want to add this new SIN to DataBase?(y/n) or type 'exit' to main menu ").strip()
					if truth_val == "exit": 
						return None, None, None, None, None
				truth_val = truth_val.lower()
				
				if truth_val == 'y':            		# If yes, ask for personal infos.	
					new_people1d = []
					new_sin.append(owner_id)
					new_people1d.append(owner_id)
					name = input("Name? ").strip()
					if name == "": 
						name = None
					new_people1d.append(name)

					height = input("Height? ").strip()
					if height == "": 
						height = None
					else:
						height = float("{0:.2f}".format(float(height)))
					new_people1d.append(height)

					weight = input("Weight? ")
					if weight == "": 
						weight = None
					else:
						weight = float("{0:.2f}".format(float(weight)))
					new_people1d.append(weight)

					eyecolor = input("Eyecolor? ").strip()
					if eyecolor == "": 
						eyecolor = None
					new_people1d.append(eyecolor)
					haircolor = input("Haircolor? ").strip()
					if haircolor == "": 
						haircolor = None
					new_people1d.append(haircolor)
					addr = input("Address? ").strip()
					if addr == "": 
						addr = None
					new_people1d.append(addr)
					gender = input("Gender?(m/f) ").strip()
					while gender not in ['m','f','M','F']:
						gender = input("Invalid input. Gender?(m/f) ").strip()
					gender = gender.lower()
					new_people1d.append(gender)
					birthday = input("Birthday? (format ex. 01-Jan-16) ").strip()
					if birthday == "":
						birthday = None
					new_people1d.append(birthday)


					new_people2d.append(new_people1d)
					break

				elif truth_val == 'n':			# If no, ask for a valid SIN.
					owner_id = input("Owner ID? or type 'exit' to main menu ").strip()
					if owner_id == "exit": 
						return None, None, None, None, None

				
			

#---------------Primary Owner?---------------------------------------------------------------------------------------------------
		is_primary_owner = input("Primary Owner?(y/n) ").strip()
		while is_primary_owner not in ['y','n','Y','N']:
			is_primary_owner = input("Invalid input. Primary Owner?(y/n) ").strip()

		is_primary_owner = is_primary_owner.lower()
#------------------------------------------------------------------------------------------------------------------
		oid.append(owner_id) 					# Append Owner ID
		ipo.append(is_primary_owner)				# Append Primary?

#---------------------------Generate all data in correct format---------------------------------------------------------------------------------------	
	vehicle_data = [(serial_no, maker, model, year, color, type_id)]			
	new_sin_data = [(new_people2d[k][0], new_people2d[k][1], new_people2d[k][2], new_people2d[k][3], new_people2d[k][4], 
				new_people2d[k][5], new_people2d[k][6], new_people2d[k][7], new_people2d[k][8]) for k in range(len(new_people2d))] 				
	owner_data = [(oid[j], serial_no, ipo[j]) for j in range(number_of_owner)]		
	return vehicle_data, owner_data, new_sin_data, number_of_owner, len(new_people2d)

#------------------------------------------------------------------------------------------------------------------


# This component is used to register a new vehicle by an auto registration officer. By a new vehicle, we mean a vehicle that has not been registered in the database. The component shall allow an officer to enter the detailed information about the vehicle and personal information about its new owners, if it is not in the database. You may assume that all the information about vehicle types has been loaded in the initial database.
def VehicleRegistration(curs,connection):
	
		
		#-------------------------------New Vehicle Registration---------------------------------------------------------------------
		# executing queries and get data
		curs.execute("SELECT * from vehicle_type")
		vtrows = curs.fetchall()	
		curs.execute("SELECT serial_no from vehicle")
		vrows = curs.fetchall()		
		curs.execute("SELECT sin from people")
		sinrows = curs.fetchall()


		# get user data	
		vehicle_data, owner_data, new_sin_data, number_of_owner, number_of_new_sin = nvr_getdata(vtrows,vrows,sinrows)
		if vehicle_data == None and owner_data == None and  new_sin_data == None and  number_of_owner == None and  number_of_new_sin  == None:
			print("NOW EXIT TO MAIN MENU")
		else:
			# get confirmation
			print("")
			confirm = input("Confirm?(y/n) ")								
			while confirm not in ['y','n','Y','N']:
					confirm = input("Invalid input. Confirm?(y/n) ").strip()
			if confirm == "y" or confirm == "Y":		
			
				# Insert values for vehicle.
				curs.bindarraysize = 1
				curs.setinputsizes(15, 20, 20, int, 10, int)
				curs.executemany("INSERT INTO vehicle(serial_no, maker, model, year, color, type_id) "
						    "VALUES (:1, :2, :3, :4, :5, :6)", vehicle_data)
				connection.commit()
				
				# If user wants to add new SIN, insert values for new SIN.
				if number_of_new_sin > 0:
					curs.bindarraysize = number_of_new_sin
					curs.setinputsizes(15, 40, float, float, 10, 10, 50, 1, 7)
					curs.executemany("INSERT INTO people(sin, name, height, weight, eyecolor, haircolor, addr, gender, birthday) "
							    "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", new_sin_data)
					connection.commit()

				# Insert values for owner.
				curs.bindarraysize = number_of_owner
				curs.setinputsizes(15, 15, 1)
				curs.executemany("INSERT INTO owner(owner_id, vehicle_id, is_primary_owner) "
				"VALUES (:1, :2, :3)", owner_data)			
				connection.commit()
				
				print("INSERT SUCCESS!")
		#----------------------------------------------------------------------------------------------------------------------------
		







