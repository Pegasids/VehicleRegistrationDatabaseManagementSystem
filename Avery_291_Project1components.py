"""
this contains 4 functions which should be functional if copied and pasted into the main file.
Populate_the_shit(curs) is the only function which is still not yet defined. 
Hoping to work on this and have this up soemtime tomorrow or the day after - Avery
"""


import sys
import cx_Oracle


def Create_all_the_tables(curs):
   '''
   drop all previously created tables and create them new from scratch
   '''

   tables = ["owner","auto_sale", "restriction","driving_condition","ticket","ticket_type","vehicle","vehicle_type","drive_licence","people"]
   for i in tables:
      curs.execute("drop table {}".format(i))

   curs.execute("create table people "
   "(sin CHAR(15), name VARCHAR(40), height number(5,2), weight number(5,2),"
   "eyecolor VARCHAR (10), haircolor VARCHAR(10), addr VARCHAR2(50), gender CHAR,"
   "birthday      DATE,"
   "PRIMARY KEY (sin), CHECK ( gender IN ('m', 'f') ))")

   curs.execute("create table drive_licence "
   "(licence_no CHAR(15), sin char(15), class VARCHAR(10), photo BLOB,"
   "issuing_date DATE, expiring_date DATE,"
   "PRIMARY KEY (licence_no), UNIQUE (sin), FOREIGN KEY (sin) REFERENCES people ON DELETE CASCADE)")   

   curs.execute("create table drive_condition "
   "(c_id INTEGER, description VARCHAR(1024),"
   "PRIMARY KEY (c_id))")

   curs.execute("create table restriction "
   "(licence_no   CHAR(15), r_id INTEGER,"
   "PRIMARY KEY (licence_no, r_id), FOREIGN KEY (licence_no) REFERENCES drive_licence,"
   "FOREIGN KEY (r_id) REFERENCES driving_condition)")

   curs.execute("create table vehicle_type "
   "(type_id integer, type CHAR(10),"
   "PRIMARY KEY (type_id))")

   curs.execute("create table vehicle "
   "(serial_no CHAR(15), maker VARCHAR(20), model VARCHAR(20), year umber(4,0),"
   "color VARCHAR(10), type_id integer,"
   "PRIMARY KEY (serial_no),FOREIGN KEY (type_id) REFERENCES vehicle_type)")

   curs.execute("create table owner "
   "(owner_id CHAR(15), vehicle_id CHAR(15), is_primary_owner CHAR(1),"
   "PRIMARY KEY (owner_id, vehicle_id),FOREIGN KEY (owner_id) REFERENCES people,"
   "FOREIGN KEY (vehicle_id) REFERENCES vehicle, CHECK ( is_primary_owner IN ('y', 'n')))")

   curs.execute("create table auto_sale "
   "(transaction_id int, seller_id CHAR(15), buyer_id CHAR(15), vehicle_id CHAR(15),"
   "s_date date, price numeric(9,2),"
   "PRIMARY KEY (transaction_id), FOREIGN KEY (seller_id) REFERENCES people,"
   "FOREIGN KEY (buyer_id) REFERENCES people, FOREIGN KEY (vehicle_id) REFERENCES vehicle)")

   curs.execute("create table ticket_type "
   "(vtype CHAR(10), fine number(5,2),"
   "PRIMARY KEY (vtype))")

   curs.execute("create table ticket "
   "(ticket_no int, violator_no CHAR(15), vehicle_id CHAR(15), office_no CHAR(15),"
   "vtype char(10), vdate  date, place varchar(20), descriptions varchar(1024),"
   "PRIMARY KEY (ticket_no), FOREIGN KEY (vtype) REFERENCES ticket_type,"
   "FOREIGN KEY (violator_no) REFERENCES people ON DELETE CASCADE, "
   "FOREIGN KEY (vehicle_id)  REFERENCES vehicle,"
   "FOREIGN KEY (office_no) REFERENCES people ON DELETE CASCADE)")

   connection.commit()


def Populate_the_shit(curs):
   '''
   function which populates our database with tuples
   '''

   data_peopletable =   [('111111111111111', "John Oliver", 167.23, 63, "blue", "black", "8407 63 Ave Edmonton", "m", "02-09-1997"),
                        ('111111111111112',"Geana Davis",160.99, 55.6,"black","black", "10108 88 Ave Edmonton", "f", "09-09-1990"),
                        ("111111111111113", "Brock Helsing", 159.43, 67.96, "black", "black", "7648 87 Street Edmonton", "m", "02-01-1900" ),
                        ("111111111111114", "Lena Nicole", 147.64, 58.45, "black", "blonde", "19238 28 Ave Edmonton", "f", '08-03-1990'),
                        ("111111111111115", 'Jacob Black', 189.76, 88.78, "green", 'blonde', "193 34 Ave Edmonton", 'm', '03-04-1980'),
                        ("111111111111116", 'Nicole Turner', 178.89, 67.87, 'black', 'blonde', "234 85 Street Edmonton", 'f', '04-06-1996'),
                        ("111111111111117", 'Amber Li', 165.56, 57.89, 'black', 'black', '246 78 Street Edmonton', 'f', '03-11-1993'),
                        ("111111111111118", 'Nadya Sannay', 155.65, 57.23, 'black', 'black', '1192 65 Street Edmonton', 'f', '07-05-1996'),
                        ("111111111111119", 'Brenda Lee', 150.56, 58.78, 'black', 'black', '1829 93 Ave Edmonton', 'f', '03-02-1990'),
                        ("111111111111120", 'Isaac Newt', 170.42, 63.45, 'blue', 'blonde', '127 34 Street Edmonton', 'm', '03-02-1993'),
                        ('111111111111121', 'Lana Lang', 170.01, 60.32, 'black', 'blonde', '1783 92 Ave Edmonton', 'f', '12-03-1991'),
                        ('111111111111122', 'Wolfgang Adolphus', 188.87, 90.21, 'black', 'black', '18336 43 Ave Edmonton', 'm', '23-04-1992'),
                        ('111111111111123', 'Staffan Lundell', 178.56, 74,34, 'blue', 'blonde', '19345 26 Street Edmonton', 'm', '19-5-1996'),
                        ('111111111111124', 'Ronia Rovarsdotter', 165.45, 69.54, 'blue', 'black', '1839 85 Ave Edmonton', 'f', '27-01-1990'),
                        ('111111111111125', 'Pippi Langstrump', 176.45,75.45, 'blue', 'blonde', '1920 73 Ave Edmonton', 'f', '15-07-1995')]
   curs.bindarraysize = 15
   curs.setinputsizes(15, 40, float, float, 10,10,50,1,"DATE")
   curs.executemany("INSERT INTO people(sin, name, height, weight, eyecolor, haircolor, addr, gender,birthday) "
                                 "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", data_peopletable)


   ####################################################################################################################################################################


   data_drivelicencetable =  [('100000000000001', '111111111111111','A', 'PHOTO', '01-01-2013', '01-01-2018'),
                              ('100000000000002', '111111111111112', 'A', 'PHOTO', '02-01-2010', '02-01-2015'),
                              ('100000000000003', '111111111111113', 'A', 'PHOTO', '03-01-2015', '03-01-2020'),
                              ('100000000000004', '111111111111114', 'B', "PHOTO", '12-02-2014', '12-02-2019'),
                              ('100000000000005', '111111111111115', 'A', 'PHOTO', '15-06-2013', '15-06-2018'),
                              ('100000000000006', '111111111111116', 'A', 'PHOTO', '13-09-2012', '13-09-2017'),
                              ('100000000000007', '111111111111117', 'C', 'PHOTO', '03-03-2015', '03-03-2020'),
                              ('100000000000008', '111111111111118', 'A', 'PHOTO', '03-01-2013', '03-01-2018'),
                              ('100000000000009', '111111111111119', 'B', 'PHOTO', '02-01-2012', '02-01-2017'), 
                              ('100000000000010', '111111111111120', 'D', 'PHOTO', '01-01-2010', '01-01-2015'),
                              ('100000000000011', '111111111111121', 'A', 'PHOTO', '04-06-2013', '04-06-2018'),
                              ('100000000000012', '111111111111122', 'A', 'PHOTO', '06-02-2016', '06-02-2021'),
                              ('100000000000013', '111111111111123', 'B', 'PHOTO', '07-03-2015', '07-03-2020'), 
                              ('100000000000014', '111111111111124', 'A', 'PHOTO', '08-03-2014', '08-03-2019'),
                              ('100000000000015', '111111111111125', 'D', 'photo', '08-07-2012', '08-07-2017')]
   curs.bindarraysize = 15
   curs.setinputsizes(15, 15, 10, "BLOB", "DATE","DATE")
   curs.executemany("INSERT INTO drive_licence(licence_no,sin,class,photo,issuing_date, expiring_date) "
                                 "VALUES (:1, :2, :3, :4, :5, :6)", data_drivelicencetable)


   ############################################################################################################################################################################

   data_drivecondition = [(0, "operator must wear glasses at all times"),
                           (1, "Operator must not drive after 6pm"),
                           (2,"Operator must have special provisions"),
                           (3,"operator must drive only for 2 hours"),
                           (4,"Operator must be a Swifty")]
   curs.bindarraysize = 5
   curs.setinputsizes(int, 1024)
   curs.executemany("INSERT INTO driving_condition(c_id, description)"
                                 "VALUES(:1,:2)", data_drivecondition)


   #############################################################################################################################################

   data_restrictiontable =   [('100000000000015', 1),
                              ('100000000000010',1),
                              ('100000000000007',2),
                              ('100000000000003',0),
                              ('100000000000004', 4),
                              ('100000000000014', 1),
                              ('100000000000010', 4)]
   curs.bindarraysize = 7
   curs.setinputsizes(15,int)
   curs.executemany("INSERT INTO restriction(licence_no, r_id)"
                                 "VALUES(:1,:2)", data_restrictiontable)


def LicenceRegistration(curs):
   """
   This component is used to record the information needed to issuing a 
   drive licence, including the personal information and a picture for 
   the driver. You may assume that all the image files are stored in a 
   local disk system.
   """
   collection_of_sin_from_people_table = set()

   curs.execute("SELECT sin from people")
   rows = curs.fetchall()
   for r in rows:
      collection_of_sin_from_people_table.add(r)

   sin = input("please enter sin number")

   while sin =='':
      sin = input("empty sin, please enter sin again")


   if sin not in collection_of_sin_from_people_table:
      choice = input("no sin found, would you like to add new person into people table? y/n")
      if choice =='y':
         p_name = input("please enter people name")
         p_height = input("please enter height")
         p_weight = input("please enter weight")
         p_eyecolor = input("please enter eyecolor")
         p_haircolor = input("please enter haircolor")
         p_addr = input("please enter address")
         p_gender = input("please enter gender. m/f")
         p_birthday = input("please enter birthday")
         curs.execute("INSERT INTO people VALUES({},{},{},{},{},{},{},{},{})".format(sin,p_name,p_height,p_weight,p_eyecolor,p_haircolor,p_addr,p_gender,p_birthday))

         licence_no = input("please enter license number")
         classs = input("please enter class")
         photo = input("please enter photo")
         issuing_date = input("please enter issuing date")
         expiring_date = input("please enter expry date")
         curs.execute("INSERT INTO drive_licence VALUES({},{},{},{},{},{})".format(licence_no,sin,classs,photo,issuing_date,expiring_date))

      elif choice =='n':
         exit_or_redo = input("would you like to reinput the sin number or exit driver licence registration input? input 'redo' or 'exit'")
         if exit_or_redo == 'exit':
            return 0
         elif exit_or_redo =='redo':
            driver_licence_registration()
   else:
      licence_no = input("please enter license number")
      classs = input("please enter class")
      photo = input("please enter photo")
      issuing_date = input("please enter issuing date")
      expiring_date = input("please enter expry date")
      curs.execute("INSERT INTO drive_licence VALUES({},{},{},{},{},{})".format(licence_no,sin,classs,photo,issuing_date,expiring_date))


def ViolationRecord(curs):
   '''
   This component is used by a police officer to issue a traffic ticket and 
   record the violation. You may assume that all the information about 
   ticket_type has been loaded in the initial database.
   '''

   col_violator_sin__people = set()
   col_veh_id__vehicle = set()
   col_off_no__people = set()
   col_tick_type__ticket_type = set()
   col_tick_no__ticket = set()

   curs.execute("SELECT ticket_no from ticket")
   rows = curs.fetchall()
   for r in rows:
      col_tick_no__ticket.add(r)

   curs.execute("SELECT sin from people")
   rows = curs.fetchall()
   for r in rows:
      col_violator_sin__people.add(r)
      col_off_no__people.add(r)

   curs.execute("SELECT vehicle_id from vehicle")
   rows = curs.fetchall()
   for r in rows:
      col_veh_id__vehicle.add(r)

   curs.execute("SELECT vtype from ticket_type")
   rows = curs.fetchall()
   for r in rows:
      col_tick_type__ticket_type.add(r)


   ticker_no = input("please enter ticket number")
   while ticker_no in col_tick_no__ticket :
      ticker_no = input("ticket number must be unique")


   violator_no = input("please enter violator no")
   while violator_no not in (col_violator_sin__people):
      violator_no = input("no such violator exists. please reinput violator_no")

   vehicle_id = input("pleaseenter vehicle id")
   while vehicle_id not in col_veh_id__vehicle:
      vehicle_id = input("no such vehicle exists. please reenter vehicle id")

   office_no = input("please enter officier number")
   while office_no not in col_off_no__people:
      office_no = input("no such person exists, please reeneter officer number")

   vtype = input("please enter violation type")
   while vtype not in col_tick_type__ticket_type:
      vtype = input("no such type, please reenter violation type")

   vdate = input("please enter violation date")
   place = input("please enter violation place")
   description = input("please enter description")

   print ("values for to be inserted: {},{},{},{},{},{},{},{}").format(ticker_no,violator_no,vehicle_id,office_no,vtype,vdate,place,description)
   confirmation = input("confirm data entry. y/n")
   if confirmation == 'y':
      curs.execute("INSERT INTO ticket VALUES({},{},{},{},{},{},{},{})".format(ticker_no,violator_no,vehicle_id,office_no,vtype,vdate,place,description))
   elif confirmation == 'n':
      redo_of_exit = input("redo or exit?")
      if redo_of_exit == 'exit':
         return 0
      elif redo_of_exit == 'redo':
         ViolationRecord()


def Search1(curs):
   '''
   List the name, licence_no, addr, birthday, driving class, driving_condition, 
   and the expiring_data of a driver by entering either a licence_no or a given name. 
   It shall display all the entries if a duplicate name is given.
   '''
   curs.execute("SELECT name from people")
   s1_col_pname = curs.fetchall()

   curs.execute("SELECT licence_no FROM drive_licence")
   s1_col_dllicence = curs.fetchall()

   search_input = input("enter search term please")

   if (search_input in s1_col_pname) or (search_input in s1_col_dllicence):
      curs.execute('''SELECT p.name, dl.licence_no, p.addr, p.birthday, dl.class, dr.description, dl.expiring_date
                  FROM people p, drive_licence dl, driveing_condition dc, restriction r
                  WHERE dl.sin=p.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id
                  ''')
      s1_result = curs.fetchall()
      for r in s1_result:
         print (r)

   else:
      redo_or_exit = input("No results found. Redo search or exit to search menu? redo/exit")
      if redo_or_exit =='redo':
         Search1(curs)
      elif redo_or_exit == 'exit':
         return 0


def Search2(curs):
   '''
   List all violation records received by a person if  the drive 
   licence_no or sin of a person  is entered.
   '''
   curs.execute("SELECT licence_no FROM drive_licence")
   s2_col_dllicence = curs.fetchall() #list contains all licence_no from drive_licence table
   curs.execute("SELECT sin FROM people")
   s2_col_psin = curs.fetchall() # list contains all sin number from people table


   search_input = input("enter sin number or licence number please")

   if (search_input in s2_col_psin) or (search_input in s2_col_dllicence):
      curs.execute('''
                  SELECT p.name, dl.licence_no, t.ticket_no, t.vehicle_id, t.vtype, t.vdate, t.place, t.descriptions, tt.fine
                  FROM ticket t, ticket_type tt, people p, drive_licence dl
                  WHERE p.sin = t.violator_no AND p.sin = dl.sin AND tt.vtype = t.vtype
                  ''')
      s2_result = curs.fetchall()
      for r in s2_result:
         print(r)

   else:
      redo_or_exit = input("No results found. Redo search or exit to search menu? redo/exit")
      if redo_or_exit =='redo':
         Search2(curs)
      elif redo_or_exit == 'exit':
         return 0


def Search3(curs): #the sql query hasn't been built yet. Will get to that eventually, unless you guys there before me
   '''
   Print out the vehicle_history, including the number of times that a vehicle has 
   been changed hand, the average price, and the number of violations it has been 
   involved by entering the vehicle's serial number.
   '''
   curs.execute("SELECT serial_no FROM vehicle")
   s3_col_vserial = curs.fetchall()

   search_input = input("Enter vehicle serial number")

   if search_input in s3_col_vserial:
      pass
   else:
      redo_or_exit = input("No results found. Redo search or exit to search menu? redo/exit")
      if redo_or_exit =='redo':
         Search3(curs)
      elif redo_or_exit == 'exit':
         return 0





 



