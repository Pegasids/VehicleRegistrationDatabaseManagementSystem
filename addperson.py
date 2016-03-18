# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# File from introduction to cx_oracle

import sys
import cx_Oracle # The package used for accessing Oracle in Python
import getpass # The package for getting password from user without displaying it

# Function takes owner id and returns the data
def add_sin(owner_id):
	
#--------------------------------------------------------Owner ID----------------------------------------------------
	new_people2d = [];
	new_people1d = []
	new_people1d.append(owner_id)

	# Gets the name
	name = input("Name? ").strip()
	if name == "": 
		name = None
	new_people1d.append(name)

	# Gets the height
	height = input("Height? ").strip()
	if height == "": 
		height = None
	else:
		height = float("{0:.2f}".format(float(height))) # Precision of 2
	new_people1d.append(height)

	# Gets the weight
	weight = input("Weight? ")
	if weight == "": 
		weight = None
	else:
		weight = float("{0:.2f}".format(float(weight))) # Precision of 2
	new_people1d.append(weight)

	# Gets the eyecolor
	eyecolor = input("Eyecolor? ").strip()
	if eyecolor == "": 
		eyecolor = None
	new_people1d.append(eyecolor)

	# Gets the haircolor
	haircolor = input("Haircolor? ").strip()
	if haircolor == "": 
		haircolor = None
	new_people1d.append(haircolor)

	# Gets the address
	addr = input("Address? ").strip()
	if addr == "": 
		addr = None
	new_people1d.append(addr)

	# Gets the gender
	gender = input("Gender?(m/f) ").strip()
	while gender not in ['m','f','M','F']:
		gender = input("Invalid input. Gender?(m/f) ").strip()
	gender = gender.lower()
	new_people1d.append(gender)

	# Gets the birthday
	birthday = input("Birthday? (format ex. 01-Jan-16) ").strip()
	if birthday == "":
		birthday = None
	new_people1d.append(birthday)
	new_people2d.append(new_people1d)

#----------------------------------------------------Return array data---------------------------------------------
	new_sin_data = [(new_people2d[k][0], new_people2d[k][1], new_people2d[k][2], new_people2d[k][3], new_people2d[k][4], 
				new_people2d[k][5], new_people2d[k][6], new_people2d[k][7], new_people2d[k][8]) for k in range(len(new_people2d))] 						
	return new_sin_data