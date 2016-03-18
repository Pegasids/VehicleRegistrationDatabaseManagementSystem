def Search1(curs,connection):
   '''
   List the name, licence_no, addr, birthday, driving class, driving_condition, 
   and the expiring_data of a driver by entering either a licence_no or a given name. 
   It shall display all the entries if a duplicate name is given.
   '''

   curs.execute("SELECT name from people")
   s1_col_pname = curs.fetchall()
   namelist = []
   for row in s1_col_pname:
      namelist.append(row[0].strip())

   curs.execute("SELECT licence_no FROM drive_licence")
   s1_col_dllicence = curs.fetchall()
   licencelist = []
   for row in s1_col_dllicence:
      licencelist.append(row[0].strip())

   ask = input("Do you want to enter a licence number or a name? (1/2)\n")
   while ask in ['1', '2']:
      if ask == '1':
         search_input = input("enter search term")
         if search_input in licencelist:
            curs.execute("SELECT p.name, dl.licence_no, p.addr, TO_CHAR(p.birthday, 'YYYY-MM-DD'), dl.class, dc.description, TO_CHAR(dl.expiring_date, 'YYYY-MM-DD') "
                    "from people p, drive_licence dl, driving_condition dc, restriction dr " +
                    "where dl.sin = p.sin and dl.licence_no = '" + search_input + "' and dr.licence_no = '" + search_input + "' and dr.r_id = dc.c_id")
         output = curs.fetchall()
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

      elif ask == '2':
         search_input = input("input search term")
         if search_input in namelist:
            print("hi")
            curs.execute("SELECT p.name, dl.licence_no, p.addr, TO_CHAR(p.birthday, 'YYYY-MM-DD'), dl.class, dc.description, TO_CHAR(dl.expiring_date, 'YYYY-MM-DD') " +
                    "from people p, drive_licence dl, driving_condition dc, restriction dr " +
                    "where p.name = '" + search_input + "' and dl.sin = p.sin and dl.licence_no = dr.licence_no and dr.r_id = dc.c_id")
            output = curs.fetchall()
            print("output", output)
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
         ask = 0
      else:
         redo = input("No results found. Redo search or exit to search menu? Redo/Exit")
         if redo == 'redo':
            Search1(curs)
         else:
            return