# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# File from introduction to cx_oracle



import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

# function takes Owner ID, return data.
def add_sin(owner_id):
#-------Enter Vehicle Infos-----------------------------------------------------------------------------------------------------------	
	new_people2d = [];

#---------------Owner ID--------------------------------------------------------------------------------------------------
	new_people1d = []
	new_people1d.append(owner_id)
	name = input("Name? ").strip()
	if name == "": 
		name = None
	new_people1d.append(name)
	height = input("Height? ").strip()
	if height == "": 
		height = None
	else:
		height = float("{0:.2f}".format(float(height))
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
					


#------------------------------------------------------------------------------------------------------------------	
	new_sin_data = [(new_people2d[k][0], new_people2d[k][1], new_people2d[k][2], new_people2d[k][3], new_people2d[k][4], 
				new_people2d[k][5], new_people2d[k][6], new_people2d[k][7], new_people2d[k][8]) for k in range(len(new_people2d))] 						
	return new_sin_data

#------------------------------------------------------------------------------------------------------------------




