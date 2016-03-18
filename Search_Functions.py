def Search1(curs, connection):
   '''
   List the name, licence_no, addr, birthday, driving class, driving_condition, 
   and the expiring_data of a driver by entering either a licence_no or a given name. 
   It shall display all the entries if a duplicate name is given.
   '''

   # Gets a list of the names in the database
   curs.execute("SELECT name from people p, drive_licence dl where p.sin = dl.sin")
   s1_col_pname = curs.fetchall()
   namelist = []
   for row in s1_col_pname:
      namelist.append(row[0].strip())

   # Gets a list of the licence numbers in the database
   curs.execute("SELECT licence_no FROM drive_licence")
   s1_col_dllicence = curs.fetchall()
   licencelist = []
   for row in s1_col_dllicence:
      licencelist.append(row[0].strip())

   # Asks if they want to input a licence number or a name
   # Uses search queries to retrieve relevant information 
   # To output into the console
   ask = input("Do you want to enter a licence number or a name? (1/2)\n")
   while ask not in ['1', '2']:
      ask = input("Invalid Input. Licence number or name? (1/2)\n")

   # Licence number inputs
   if ask == '1':
      search_input = input("Input search term: ")
      if search_input == "":
         print("Invalid Input. Input a new search term: ")

      # Checks if the user input is a real licence in the list
      elif search_input in licencelist:
         curs.execute("SELECT p.name, dl.licence_no, p.addr, TO_CHAR(p.birthday, 'YYYY-MM-DD'), dl.class, dc.description, TO_CHAR(dl.expiring_date, 'YYYY-MM-DD') "
               "from people p, drive_licence dl, driving_condition dc, restriction dr " +
               "where dl.sin = p.sin and dl.licence_no = '" + search_input + "' and dr.licence_no = '" + search_input + "' and dr.r_id = dc.c_id")
         output = curs.fetchall()

         # If the query returns empty because the driver with the associated
         # Licence number does not have a driving condition
         if output == []:
            curs.execute("SELECT p.name, dl.licence_no, p.addr, TO_CHAR(p.birthday, 'YYYY-MM-DD'), dl.class, TO_CHAR(dl.expiring_date, 'YYYY-MM-DD') "
               "from people p, drive_licence dl "
               "where dl.sin = p.sin and dl.licence_no = '" + search_input + "'")
            output = curs.fetchall()

            # Prints the new ouput from the new query
            for row in output:
               print("\n")
               display = []
               for i in row:
                  display.append(i.strip())
               print("Driver Name: " + display[0])
               print("Licence Number: " + display[1])
               print("Address: " + display[2])
               print("Birthday: " + display[3])
               print("Driving Class: " + display[4])
               print("Driving Condition: None ")
               print("Expiring Date: " + display[5])
            return

         # If they do have a driving condition print the relevant information
         else:
            for row in output:
               print("\n")
               display = []
               for i in row:
                  display.append(i.strip())
               print("Driver Name: " + display[0])
               print("Licence Number: " + display[1])
               print("Address: " + display[2])
               print("Birthday: " + display[3])
               print("Driving Class: " + display[4])
               print("Driving Condition: " + display[5])
               print("Expiring Date: " + display[6])
            return

      # If the licence number is not in the database return to the menu
      else:
         redo = input("No results found. Redo search or exit to search menu? Redo/Exit")
         if redo == 'redo':
            Search1(curs, connection)
         else:
            return

   # Name Inputs
   else:
      search_input = input("Input search term: ")
      if search_input == "":
         print("Invalid Input. Input a new search term: ")

      # Checks to see if the user input is a real name in the database
      elif search_input in namelist:
         curs.execute("SELECT p.name, dl.licence_no, p.addr, TO_CHAR(p.birthday, 'YYYY-MM-DD'), dl.class, dc.description, TO_CHAR(dl.expiring_date, 'YYYY-MM-DD') " +
               "from people p, drive_licence dl, driving_condition dc, restriction dr " +
               "where p.name = '" + search_input + "' and dl.sin = p.sin and dl.licence_no = dr.licence_no and dr.r_id = dc.c_id")
         output = curs.fetchall()

         # If they do not have a driving condition
         if output == []:
            curs.execute("SELECT p.name, dl.licence_no, p.addr, TO_CHAR(p.birthday, 'YYYY-MM-DD'), dl.class, TO_CHAR(dl.expiring_date, 'YYYY-MM-DD') " 
               "from people p, drive_licence dl " 
               "where p.name = '" + search_input + "' and dl.sin = p.sin ")
            output = curs.fetchall()

            # Print the ouput from the new query
            for row in output:
               print("\n")
               display = []
               for i in row:
                  display.append(i.strip())
               print("Driver Name: " + display[0])
               print("Licence Number: " + display[1])
               print("Address: " + display[2])
               print("Birthday: " + display[3])
               print("Driving Class: " + display[4])
               print("Driving Condition: None")
               print("Expiring Date: " + display[5])
            return

         # If they do have a driving condition print the relevant information
         else:
            for row in output:
               print("\n")
               display = []
               for i in row:
                  display.append(i.strip())
               print("Driver Name: " + display[0])
               print("Licence Number: " + display[1])
               print("Address: " + display[2])
               print("Birthday: " + display[3])
               print("Driving Class: " + display[4])
               print("Driving Condition: " + display[5])
               print("Expiring Date: " + display[6])
            return

      # If no results are found
      else:
         redo = input("No results found. Redo search or exit to search menu? Redo/Exit ")
         if redo == 'redo':
            Search1(curs, connection)
         else:
            return



# List all violation records received by a person if the drive licence_no or sin of a person  is entered.
def Search2(curs,connection):

   curs.execute("SELECT sin FROM people")    # Add all the sin from people to a list.
   all_sin = curs.fetchall()  
   sin_lst = []   
   for sin in all_sin:
      sin_lst.append(sin[0].strip())

   curs.execute("SELECT licence_no FROM drive_licence")  # Add all the licence_no from drive_licence to a list.
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
      sin = input("SIN? ").strip()  # Ask for SIN.
      while sin not in sin_lst:  # Raise error if SIN doesnt exist.
         sin = input("SIN doesn't exist in database! Enter a valid SIN or type 'exit' to main menu ").strip()
         if sin == "exit":
            return None
      
      # Run the query.
      curs.execute("SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, TO_CHAR(t.vdate, 'YYYY-MM-DD'), t.place, t.descriptions FROM ticket t where t.violator_no = '" + sin + "'")
      # Print all the outputs.
      all_vr = curs.fetchall()
      if all_vr == []:  # If SIN exist but doesn't have any violation record , do the following.
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
      dln = input("Driver Licence Number? ").strip()     # Ask for Licence_no.
      while dln not in dln_lst:           # Raise error if Licence_no doesnt exist
         dln = input("DLN doesn't exist in database! Enter a valid Driver Licence Number or type 'exit' to main menu ").strip()
         if dln == "exit":
            return None

      # Run the query.
      curs.execute("select d.licence_no, t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, TO_CHAR(t.vdate, 'YYYY-MM-DD'), t.place, t.descriptions from ticket t, drive_licence d where d.sin = t.violator_no and d.licence_no = '" + dln + "'")

      # Print all the outputs.
      all_vr = curs.fetchall()
      if all_vr == []:  # If Licence_no exist but doesn't have any violation record , do the following.
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
   


# Print out the vehicle_history, including the number of times that a vehicle has been changed hand, the average price, and the number of violations it has been involved by entering the vehicle's serial number.
def Search3(curs,connection):
   
   curs.execute("SELECT serial_no FROM vehicle")         # Add all the serial_no from vehicle into a list to check for any invalid serial_no.
   s3_col_vserial = curs.fetchall() 
   vrowlst = []   
   for vrow in s3_col_vserial:
      vrowlst.append(vrow[0].strip())

   serial_no = input("Enter vehicle serial number: ").strip()  # Ask user to enter a serial_no.
   while serial_no == "" or serial_no not in vrowlst:    # Raise error if user enter blank or non-existing serial_no.
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
