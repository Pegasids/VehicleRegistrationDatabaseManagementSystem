# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# File from introduction to cx_oracle

import sys
import cx_Oracle # The package used for accessing Oracle in Python
import getpass # The package for getting password from user without displaying it\

# Imports addperson to add a new person 
from addperson_nathan import *

#------------------------------------------------Auto Transaction----------------------------------------------------
def AutoTransaction(curs, connection):
	# Execute the queries to get the data
		curs.execute("SELECT owner_id from owner")
		orows = curs.fetchall()
		curs.execute("SELECT sin from people")
		sinrows = curs.fetchall()
		curs.execute("SELECT serial_no from vehicle")
		vrows = curs.fetchall()
		curs.execute("SELECT transaction_id from auto_sale")
		arows = curs.fetchall()
		
		# Get the relevant Auto Transaction data
		
		sale_data, seller_id, buyer_id, vehicle_id, sin_data = getATdata(orows, sinrows, vrows, arows, curs)

		# Get confirmation from the user
		print("")
		confirm = input("Confirm?(y/n) ")
		while confirm not in ['y','n','Y','N']:
			confirm = input("Invalid input. Confirm?(y/n) ").strip()
		if confirm == "y" or confirm == "Y":

         # If we do not input a new person execute these queries
			if sin_data == []:
				curs.setinputsizes(int, 15, 15, 15, 7, float)
				curs.execute("INSERT INTO auto_sale(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price) "
								"VALUES (:1, :2, :3, :4, :5, :6)", sale_data)
				connection.commit()
				curs.execute("UPDATE owner SET owner_id = '" + buyer_id + "' WHERE owner_id = '" + seller_id + "' and vehicle_id = '" + vehicle_id + "'")
				connection.commit()
				curs.execute("DELETE from owner WHERE vehicle_id = '" + vehicle_id + "' and owner_id != '" + buyer_id + "'")
				connection.commit()

         # Else execute these queries
			else:
				curs.setinputsizes(15, 40, float, float, 10, 10, 50, 1, 7)
				curs.execute("INSERT INTO people(sin, name, height, weight, eyecolor, haircolor, addr, gender, birthday) "
								"VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", sin_data)
				connection.commit()
				curs.setinputsizes(int, 15, 15, 15, 7, float)
				curs.execute("INSERT INTO auto_sale(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price) "
								"VALUES (:1, :2, :3, :4, :5, :6)", sale_data)
				connection.commit()
				curs.execute("UPDATE owner SET owner_id = '" + buyer_id + "' WHERE owner_id = '" + seller_id + "' and vehicle_id = '" + vehicle_id + "'")
				connection.commit()
				curs.execute("DELETE from owner WHERE vehicle_id = '" + vehicle_id + "' and owner_id != '" + buyer_id + "'")
				connection.commit()

      # If they do not confirm return to the main menu
		else:
			return

def getATdata(orows, sinrows, vrows, arows, curs):
	# --------------------- Transaction ID ---------------------
	alist = []
	for row in arows:
		alist.append(row[0])
	print("Auto Transaction")

   # Asks the user to input a new transaction ID
	trans_id = input("Transaction ID?\n").strip()
	while trans_id == "" or int(trans_id) in alist:
		if trans_id == "":
			trans_id = input("Invalid input. Enter a valid transaction id.\n").strip()
		else:
			trans_id = input("Transaction id already exists in the database. Enter a new transaction id.\n").strip()

	# --------------------- Buyer/Seller ID ---------------------
	bsequal = True
	plist = []
	olist = []
	real_sin = []

   # Gets the owners and people from the database
   # and strips them to use the relevant data
	for row in orows:
		olist.append(row[0].strip())
	for row in sinrows:
		plist.append(row[0].strip())
	while bsequal == True: 

      # Asks for the seller id and checks if they
      # do not exist or if they do not own a vehicle
		seller_id = input("Enter the seller id.\n").strip()

		while seller_id == "" or seller_id not in plist or seller_id not in olist:
			if seller_id == "":
				seller_id = input("Invalid input. Enter the seller id.\n").strip()
			elif seller_id not in plist:
				seller_id = input("Seller does not exist. Enter a new seller id.\n").strip()
			else:
				seller_id = input("Seller does not own any vehicles. Enter a new seller id.\n").strip()

      # Asks for the buyer id and checks if they exist 
      #If they do not exist add the person to the database
		buyer_id = input("Enter the buyer id.\n").strip()

		while buyer_id == "" or buyer_id not in plist:
			if buyer_id == "":
				buyer_id = input("Invalid input. Enter the buyer id.\n").strip()
			else:
				add = input("Add the new buyer to the database? Y/N.\n").strip()
				while add not in ['y', 'Y', 'n', 'N']:
					add = input("Invalid input. Add the new buyer to the database? Y/N.\n").strip()

            # Calls add add_sin from addperson and
            # appends it to return to use
				if add == 'y' or add == 'Y':
					sin_data = add_sin(buyer_id)
					real_sin = []
					for row in sin_data:
						for i in row:
							real_sin.append(i)
					break
				elif add == 'n' or add == 'N':
					buyer_id = input("Enter a new buyer id.\n").strip()
		
      # Handles case where buyer and seller id are the same
		if buyer_id == seller_id:
			print("ID of buyer and seller cannot be the same. Please enter the buyer and seller id again.\n")
			bsequal = True
		else:
			bsequal = False

	# ---------------------- Vehicle ID ------------------------
	vsequal = True
	vlist = []

   # Gets the vehicle data for use
	for row in vrows:
		vlist.append(row[0].strip())

	while vsequal == True:

      # Asks for the vehicle ID
		vehicle_id = input("Enter the vehicle id.\n").strip()
		flag = False
		count = False
		owns = []

		if vehicle_id == "":
			print("Invalid input, try again.")

      # If the vehicle id is a valid input
      # Execute query statments and check if
      # the vehicle exists in the database
		else:
			curs.execute("SELECT vehicle_id from owner")
			exist = curs.fetchall()
			curs.execute("SELECT vehicle_id from owner where owner_id = '" + seller_id + "' and vehicle_id = '" + vehicle_id + "'")
			owner = curs.fetchall()
			curs.execute("SELECT * from owner where owner_id = '" + seller_id + "' and vehicle_id = '" + vehicle_id + "' and is_primary_owner = 'y' ")
			primary = curs.fetchall()

         # Gets all owners of vehicles
			for i in owner:
				owns.append(i[0].strip())

         # Checks if the vehicle ID exists
			for a in exist:
				if vehicle_id == a[0].strip():
					count = True
			if not count:
				print("Vehicle does not exist, try again.")
				flag = True

         # Checks if the vehicle is owned by the seller
         # or if the seller is the primary owner
			if not flag:
				if vehicle_id not in owns:
					print("Vehicle is not owned by the seller, try again.")
				elif not primary:
					print("Seller is not the primary owner, try again.")
				else:
					vsequal = False

	# ------------------------- Date ---------------------------
	date = input("Enter the date of the transaction.\n").strip()

	# ------------------------- Price --------------------------
	price = input("Enter the sale price of the transaction.\n").strip()
	price = float("{0:.2f}".format(float(price)))  # Precision of 2

	sale_data = [trans_id, seller_id, buyer_id, vehicle_id, date, price]

	return sale_data, seller_id, buyer_id, vehicle_id, real_sin