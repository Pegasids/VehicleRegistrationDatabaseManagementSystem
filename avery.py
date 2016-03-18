"""
this contains 4 functions which should be functional if copied and pasted into the main file.
Populate_the_shit(curs) is the only function which is still not yet defined. 
Hoping to work on this and have this up soemtime tomorrow or the day after - Avery
"""


import sys
import cx_Oracle
import getpass



def Create_all_the_tables(curs,connection):
   '''
   drop all previously created tables and create them new from scratch
   '''

   tables = ["restriction","auto_sale", "driving_condition","ticket","ticket_type","drive_licence","owner","people","vehicle", "vehicle_type"]
   for i in tables:
      print("dropping  ", i)
      curs.execute("drop table "+str(i))
   print("PASS!")


   curs.execute("create table people "
   "(sin CHAR(15), name VARCHAR(40), height number(5,2), weight number(5,2),"
   "eyecolor VARCHAR (10), haircolor VARCHAR(10), addr VARCHAR2(50), gender CHAR,"
   "birthday      DATE,"
   "PRIMARY KEY (sin), CHECK ( gender IN ('m', 'f') ))")

   curs.execute("create table drive_licence "
   "(licence_no CHAR(15), sin char(15), class VARCHAR(10), photo CHAR(10),"
   "issuing_date DATE, expiring_date DATE,"
   "PRIMARY KEY (licence_no), UNIQUE (sin), FOREIGN KEY (sin) REFERENCES people ON DELETE CASCADE)")   

   curs.execute("create table driving_condition "
   "(c_id INTEGER, description VARCHAR(1024),"
   "PRIMARY KEY (c_id))")
   
   curs.execute("create table restriction "
   "(licence_no   CHAR(15), r_id INTEGER,"
   "PRIMARY KEY (licence_no, r_id), FOREIGN KEY (licence_no) REFERENCES drive_licence,"
   "FOREIGN KEY (r_id) REFERENCES driving_condition)"
   )


   curs.execute("create table vehicle_type "
   "(type_id integer, type CHAR(10),"
   "PRIMARY KEY (type_id))")

   curs.execute("create table vehicle "
   "(serial_no CHAR(15), maker VARCHAR(20), model VARCHAR(20), year number(4,0),"
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

   print("defining tables all done")

   connection.commit()


def Populate_the_shit(curs,connection):
   '''
   function which populates our database with tuples

   known issues: unknown format type for DATE and BLOB
   '''

   data_peopletable =   [('111111111111111', "John Oliver", 167.23, 63.32, "blue", "black", "8407 63 Ave Edmonton", "m", "02-JAN-1997"),
                         ('111111111111112',"Geana Davis",160.99, 55.63,"black","black", "10108 88 Ave Edmonton", "f", "09-SEP-1990"),
                         ("111111111111113", "Brock Helsing", 159.43, 67.96, "black", "black", "7648 87 Street Edmonton", "m", "02-DEC-1900" ),
                         ("111111111111114", "Lena Nicole", 147.64, 58.45, "black", "blonde", "19238 28 Ave Edmonton", "f", '08-FEB-1990'),
                         ("111111111111115", 'Jacob Black', 189.76, 88.78, "green", 'blonde', "193 34 Ave Edmonton", 'm', '03-JAN-1980'),
                         ("111111111111116", 'Nicole Turner', 178.89, 67.87, 'black', 'blonde', "234 85 Street Edmonton", 'f', '04-NOV-1996'),
                         ("111111111111117", 'Amber Li', 165.56, 57.89, 'black', 'black', '246 78 Street Edmonton', 'f', '03-OCT-1993'),
                         ("111111111111118", 'Nadya Sannay', 155.65, 57.23, 'black', 'black', '1192 65 Street Edmonton', 'f', '07-JAN-1996'),
                         ("111111111111119", 'Brenda Lee', 150.56, 58.78, 'black', 'black', '1829 93 Ave Edmonton', 'f', '03-OCT-1990'),
                         ("111111111111120", 'Isaac Newt', 170.42, 63.45, 'blue', 'blonde', '127 34 Street Edmonton', 'm', '03-SEP-1993'),
                         ('111111111111121', 'Lana Lang', 170.01, 60.32, 'black', 'blonde', '1783 92 Ave Edmonton', 'f', '12-DEC-1991'),
                         ('111111111111122', 'Wolfgang Adolphus', 188.87, 90.21, 'black', 'black', '18336 43 Ave Edmonton', 'm', '23-FEB-1992'),
                         ('111111111111123', 'Staffan Lundell', 178.56, 74.34, 'blue', 'blonde', '19345 26 Street Edmonton', 'm', '19-JAN-1996'),
                         ('111111111111124', 'Ronia Rovarsdotter', 165.45, 69.54, 'blue', 'black', '1839 85 Ave Edmonton', 'f', '27-FEB-1990'),
                        ('111111111111125', 'Pippi Langstrump', 176.45,75.45, 'blue', 'blonde', '1920 73 Ave Edmonton', 'f', '15-FEB-1995')]
   curs.bindarraysize = 15
   curs.setinputsizes(15, 40, float, float, 10,10,50,1,15) #position 8 is DATE! floats are number(5,2)
   curs.executemany("INSERT INTO people(sin, name, height, weight, eyecolor, haircolor, addr, gender,birthday) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", data_peopletable)


   ####################################################################################################################################################################


   data_drivelicencetable =  [('100000000000001', '111111111111111','A', '0x12', '01-JAN-2013', '01-JAN-2018'),
                              ('100000000000002', '111111111111112', 'A', 'PHOTO', '02-JAN-2010', '02-FEB-2015'),
                              ('100000000000003', '111111111111113', 'A', 'PHOTO', '03-JAN-2015', '03-JAN-2020'),
                              ('100000000000004', '111111111111114', 'B', "PHOTO", '12-FEB-2014', '12-FEB-2019'),
                              ('100000000000005', '111111111111115', 'A', 'PHOTO', '15-FEB-2013', '15-OCT-2018'),
                              ('100000000000006', '111111111111116', 'A', 'PHOTO', '13-SEP-2012', '13-DEC-2017'),
                              ('100000000000007', '111111111111117', 'C', 'PHOTO', '03-MAY-2015', '03-JAN-2020'),
                              ('100000000000008', '111111111111118', 'A', 'PHOTO', '03-JAN-2013', '03-JAN-2018'),
                              ('100000000000009', '111111111111119', 'B', 'PHOTO', '02-JAN-2012', '02-JAN-2017'), 
                              ('100000000000010', '111111111111120', 'D', 'PHOTO', '01-JAN-2010', '01-JAN-2015'),
                              ('100000000000011', '111111111111121', 'A', 'PHOTO', '04-JUN-2013', '04-SEP-2018'),
                              ('100000000000012', '111111111111122', 'A', 'PHOTO', '06-JUL-2016', '06-DEC-2021'),
                              ('100000000000013', '111111111111123', 'B', 'PHOTO', '07-DEC-2015', '07-OCT-2020'), 
                              ('100000000000014', '111111111111124', 'A', 'PHOTO', '08-SEP-2014', '08-JAN-2019'),
                              ('100000000000015', '111111111111125', 'D', '0x43', '08-OCT-2012', '08-JAN-2017')]
   curs.bindarraysize = 2
   curs.setinputsizes(15, 15, 10, 10, 10,10) #position 3 is BLOB!! position  position 4 and 5 is DATE!!
   curs.executemany("INSERT INTO drive_licence(licence_no,sin,class,photo,issuing_date, expiring_date) "
                                 "VALUES (:1, :2, :3, :4, :5, :6)", data_drivelicencetable)


   # ############################################################################################################################################################################

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






   data_vehicletypetable = [(10,"SUV"), (11,"Hatchback"), (12,"Sedan"),(13,"Truck"),(14,"Van")]
   curs.bindarraysize = 5
   curs.setinputsizes(int,10)
   curs.executemany("INSERT INTO vehicle_type(type_id, type)"
                                 "VALUES(:1,:2)", data_vehicletypetable)





   data_vehicletable = [("122222222222220", "Honda", "Civic", 2004, "blue", 12),
                        ("122222222222221","Subaru", "Crosstrek", 2014, "black", 11),
                        ("122222222222222", "Toyota", "Corolla", 2007, "white", 12),
                        ("122222222222223", "Ford", "Focus", 2007, "black", 10),
                        ("122222222222224", "BMW", "Serio", 2010, "black", 12),
                        ("122222222222225", "RAM", "Bizarro", 2009, "red", 13),
                        ("122222222222226", "Mitsubishi", "Lancer", 2009, "white", 12),
                        ("122222222222227", "Dodge", "Focus", 2002, "black", 13),
                        ("122222222222228", "Subaru", "Forrester", 2015,"green", 10),
                        ("122222222222229", "Toyota", "Camry", 2010, "black", 12),
                        ("122222222222230", "Ford", "holla", 2007,"blue", 14),
                        ("122222222222231", "Ford", "Mustang", 2014,"black", 12),
                        ("122222222222232", "Honda", "Ascend", 2008,"blue", 11),
                        ("122222222222233", "Mazda", "T1", 2010,"black", 11),
                        ("122222222222234", "ssangyong", "Nadya", 2011, "white", 14),
                        ("122222222222235", "Toyota", "Kijang", 2007, "blue", 14),
                        ("122222222222236", "tata", "Abend", 2008,"black", 13),
                        ("122222222222237", "Toyota", "Corolla", 2008,"white", 12),
                        ("122222222222238", "BMW", "Serio", 2010, "red", 12),
                        ("122222222222239", "Ford", "Focus", 2009,"black", 10),
                        ("122222222222240", "Mazda", "T2", 2015, "blue", 13),
                        ("122222222222241", "Honda", "Civic", 2009,"red", 12),
                        ("122222222222242", "Subaru", "Crosstrek", 2015,"white", 11)]
   curs.bindarraysize = 23
   curs.setinputsizes(15,20,20,int,10,int)
   curs.executemany("INSERT INTO vehicle(serial_no, maker,model,year,color,type_id)"
                                    "VALUES(:1,:2,:3,:4,:5,:6)", data_vehicletable)




   data_ownertable = [("111111111111111", "122222222222220", 'y'),
                      ("111111111111112", "122222222222221", 'y'),
                      ("111111111111113", "122222222222222", 'y'),
                      ("111111111111114", "122222222222223", 'y'),
                      ("111111111111115", "122222222222224", 'y'),
                      ("111111111111116", "122222222222225", 'y'),
                      ("111111111111117", "122222222222226", 'y'),
                      ("111111111111118", "122222222222227", 'y'),
                      ("111111111111119", "122222222222228", 'y'),
                      ("111111111111120", "122222222222229", 'y'),
                      ("111111111111121", "122222222222230", 'y'),
                      ("111111111111122", "122222222222231", 'y'),
                      ("111111111111123", "122222222222232", 'y'),
                      ("111111111111124", "122222222222233", 'y'),

                      ("111111111111125", "122222222222234", 'n'),
                      ("111111111111120", "122222222222235", 'n'),
                      ("111111111111121", "122222222222236", 'n'),
                      ("111111111111122", "122222222222237", 'n'),
                      ("111111111111123", "122222222222238", 'n'),
                      ("111111111111124", "122222222222239", 'n'),
                      ("111111111111125", "122222222222240", 'n'),

                      ("111111111111111", "122222222222234", 'y'),
                      ("111111111111112", "122222222222235", 'y'),
                      ("111111111111113", "122222222222236", 'y'),
                      ("111111111111114", "122222222222237", 'y'),
                      ("111111111111115", "122222222222238", 'y'),
                      ("111111111111116", "122222222222239", 'y'),
                      ("111111111111117", "122222222222240", 'y')]
   curs.bindarraysize = 30
   curs.setinputsizes(15,15,1)
   curs.executemany("INSERT INTO owner(owner_id, vehicle_id, is_primary_owner)"
                              "VALUES(:1,:2,:3)", data_ownertable)




   #only records sales between non-commercial individuals/entities, not sales between first-time buyers and car dealerships.
   data_auto_sale_table = [(21, "111111111111121", "111111111111113", "122222222222222", "02-FEB-2009", 15000.00),
                            (22, "111111111111120", "111111111111112", "122222222222223", "02-MAY-2010", 17000.00),
                            (23, "111111111111112", "111111111111114", "122222222222223", "09-SEP-2015", 20000.00),
                            (24, "111111111111111", "111111111111125", "122222222222234", "01-SEP-2015", 5000.00),
                            (25,"111111111111121", "111111111111112", "122222222222237", "02-MAY-2012", 5000.00),
                            (26, "111111111111122", "111111111111123", "122222222222237", "02-FEB-2013", 7000.00), 
                            (28, "111111111111120", "111111111111122", "122222222222237", "03-JAN-2015", 7500.00),
                           (27, "111111111111123", "111111111111120", "122222222222237", "04-FEB-2014", 4000.00),
                            (29, "111111111111119", "111111111111111", "122222222222220", "03-MAY-2013", 12000.00),
                           (30, "111111111111124", "111111111111115", "122222222222224", "03-FEB-2014", 10000.00)]
   curs.bindarraysize = 10
   curs.setinputsizes(int,15, 15,15,10,float) #position 4 is DATE! float is numberic(9,2)
   curs.executemany("INSERT INTO auto_sale(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price)"
                              "VALUES(:1,:2,:3,:4,:5,:6)", data_auto_sale_table)




   data_ticket_type_table = [("Speeding", 150), ("Parking", 50), ("Intersect", 200), ("Halting", 50), ("E Speeding", 350)]
   curs.bindarraysize = 5
   curs.setinputsizes(10,float) #float is number(5,2)
   curs.executemany("INSERT INTO ticket_type(vtype, fine)"
                              "VALUES(:1,:2)", data_ticket_type_table)



   data_ticket_table = [(101,"111111111111121", "122222222222230", "111111111111111", "Speeding", "03-JAN-2014", "Southampton", "He did a bad thing" ),
                        (102,"111111111111117", "122222222222226", "111111111111111", "Parking", "02-SEP-2013", "Riverbend", "Parked in a no-park zone" ),
                        (103,"111111111111124", "122222222222233", "111111111111111", "Parking", "01-MAY-2015", "Lowlands", "Parked in alley" ),
                        (104,"111111111111115", "122222222222224", "111111111111112", "Halting", "03-JAN-2012", "Marshuggah", "Mother didn't teach him nothing" ),
                        (105, "111111111111121", "122222222222230","111111111111111", "Parking", "09-FEB-2010", "Southampton", "firehydrant parking"),
                        (106, "111111111111121", "122222222222230","111111111111112", "Parking", "03-JAN-2013", "Southampton", "Parked near stop sign"),
                        (107, "111111111111119", "122222222222228", "111111111111111", "E Speeding", "02-FEB-2009", "Eastview", "sped in excess of 150km/h"),
                        (108, "111111111111113", "122222222222222", "111111111111112", "Intersect", "05-MAY-2010", "Glendon", "did non-premissible thing"),
                        (109, "111111111111113", "122222222222222", "111111111111111", "Speeding", "04-JAN-2014", "Barking", "sped through highway"),
                        (110, "111111111111113", "122222222222222", "111111111111112", "Parking", "03-DEC-2011", "Pistleton", "sped like a beast")]
   curs.bindarraysize = 10
   curs.setinputsizes(int, 15, 15,15,10,10, 20,1024) #position 6 is DATE!
   curs.executemany("INSERT INTO ticket(ticket_no, violator_no, vehicle_id, office_no, vtype,vdate,place,descriptions)"
                              "VALUES(:1,:2,:3,:4,:5,:6,:7,:8)", data_ticket_table)

   connection.commit()
   print("populating database all done")

# #TESTED and DONE! (except for photo. Create a new function and keep this as is if you'd want to correc the photo function)
# def LicenceRegistration(curs,connection):
#    """
#    This component is used to record the information needed to issuing a 
#    drive licence, including the personal information and a picture for 
#    the driver. You may assume that all the image files are stored in a 
#    local disk system.

#    known issues: Unknown format for DATE and BLOB
#    """
#    exit_flag = False
#    curs.execute("SELECT sin from people")
#    real_col = set()
#    list_sin_from_people_table = set(curs.fetchall())
#    for i in list_sin_from_people_table:
#       real_col.add(i[0].strip())
#    curs.execute("SELECT licence_no from drive_licence")
#    licence_no__drive_licence = set(curs.fetchall())
#    real_licence_no__drive_licence = set()
#    for i in licence_no__drive_licence:
#       real_licence_no__drive_licence.add(i[0].strip())



#    sin = input("please enter sin number")

#    while sin =='':
#       sin = input("empty sin, please enter sin again or type exit to exit to main menu")
#       if sin == "exit":
#         return



#    if sin not in real_col:
#       choice = input("no sin found, would you like to add new person into people table? y/n")
#       if choice =='y':
#          p_name = input("please enter people name")
#          p_height = input("please enter height")
#          p_weight = input("please enter weight")
#          p_eyecolor = input("please enter eyecolor")
#          p_haircolor = input("please enter haircolor")
#          p_addr = input("please enter address")
#          p_gender = input("please enter gender. m/f")
#          p_birthday = input("please enter birthday")
#          confirm = input("confirm entering:({},{},{},{},{},{},{},{},{}) Enter y to confirm, n to return to main menu".format(sin,p_name,p_height,p_weight,p_eyecolor,p_haircolor,p_addr,p_gender,p_birthday))
#          values = (sin,p_name,p_height,p_weight,p_eyecolor,p_haircolor,p_addr,p_gender,p_birthday)
#          if confirm == 'y':
#             curs.execute("INSERT INTO people VALUES "+str(values) )
#             connection.commit()
#          else:
#             return

#          licence_no = input("please enter license number")
#          while licence_no in real_licence_no__drive_licence:
#             licence_no = input("license number already exists, enter a unique one please")
#          classs = input("please enter class")
#          photo = input("please enter photo")
#          issuing_date = input("please enter issuing date")
#          expiring_date = input("please enter expry date")
#          confirm = input("confirm entering({},{},{},{},{},{}) enter y to confirm, n to exit to main menu".format(licence_no,sin,classs,photo,issuing_date,expiring_date))
#          if confirm == 'y':
#             curs.execute("INSERT INTO drive_licence VALUES" +str((licence_no,sin,classs,photo,issuing_date,expiring_date)))
#          else: 
#             return

#       elif choice =='n':
#          exit_or_redo = input("would you like to reinput the sin number or exit driver licence registration input? input 'redo' or 'exit'")
#          if exit_or_redo == 'exit':
#             return
#          elif exit_or_redo =='redo':
#             LicenceRegistration(curs,connection)
#    else:
#       licence_no = input("please enter license number")
#       while licence_no in real_licence_no__drive_licence:
#          licence_no = input("license must be unique! please reenter")
#       classs = input("please enter class")
#       photo = input("please enter photo name with extension")
#       issuing_date = input("please enter issuing date")
#       expiring_date = input("please enter expry date")
#       confirm = input("confirm entering({},{},{},{},{},{}) enter y to confirm, n to exit to main menu".format(licence_no,sin,classs,photo,issuing_date,expiring_date))
#       if confirm =='y':
#          curs.execute("INSERT INTO drive_licence VALUES"+str((licence_no,sin,classs,photo,issuing_date,expiring_date)))
#       else:
#          return
#    connection.commit()


#TESTED AND DONE! 100%
def ViolationRecord(curs,connection):
   '''
   This component is used by a police officer to issue a traffic ticket and 
   record the violation. You may assume that all the information about 
   ticket_type has been loaded in the initial database.
   '''


   curs.execute("SELECT ticket_no from ticket")
   col_tick_no__ticket= set(curs.fetchall())
   real_col_tick_no__ticket = set()
   for i in col_tick_no__ticket:
      real_col_tick_no__ticket.add(i[0])

   curs.execute("SELECT sin from people")
   col_sin__people = set(curs.fetchall())
   real_col_sin__people = set()
   for i in col_sin__people:
      real_col_sin__people.add(i[0].strip())


   curs.execute("SELECT serial_no from vehicle")
   col_veh_id__vehicle = set(curs.fetchall())
   real_col_veh_id__vehicle = set()
   for i in col_veh_id__vehicle:
      real_col_veh_id__vehicle.add(i[0].strip())

   curs.execute("SELECT vtype from ticket_type")
   col_tick_type__ticket_type = set(curs.fetchall())
   real_col_tick_type__ticket_type = set()
   for i in col_tick_type__ticket_type:
      real_col_tick_type__ticket_type.add(i[0].strip())


   ticker_no = int(input("please enter ticket number"))
   while ticker_no in real_col_tick_no__ticket :
      ticker_no = int(input("ticket number must be unique. reenter, or enter 'exit' to return to main menu"))
      if ticker_no == 'exit':
         return

   vehicle_id = input("please enter vehicle id")
   while vehicle_id not in real_col_veh_id__vehicle:
      vehicle_id = input("no such vehicle exists. please reenter vehicle id or type 'exit' to return to menu")
      if vehicle_id == 'exit':
         return

   primary_or_generic = input("Add to primary owner? enter yes or enter no to manually enter violator id")

   if primary_or_generic == 'no':
      violator_no = input("please enter violator no")
      while violator_no not in (real_col_sin__people):
         violator_no = input("no such violator exists. please reinput violator_no or type 'exit' to return ot main menu")
         if violator_no == 'exit':
            return
   elif primary_or_generic =='yes':
      execution = "select owner_id from owner where is_primary_owner = 'y' and vehicle_id = {}".format(vehicle_id)
      curs.execute(execution)
      primary_ownerresult = curs.fetchall()
      list_primary_owner = list()
      for i in primary_ownerresult:
         list_primary_owner.append(i[0].strip())
         violator_no = list_primary_owner[0]
   print("driver ", violator_no, "will be charged! ")

   office_no = input("please enter officier number")
   while office_no not in real_col_sin__people:
      office_no = input("no such person exists, please reeneter officer number or type 'exit' to return to menu")
      if office_no == 'exit':
         return

   vtype = input("please enter violation type")
   while vtype not in real_col_tick_type__ticket_type:
      vtype = input("no such type, please reenter violation type or type exit to return to menu")
      if vtype =='exit':
         return

   vdate = input("please enter violation date")
   place = input("please enter violation place")
   description = input("please enter description")

   print ("values for to be inserted: {},{},{},{},{},{},{},{}".format(ticker_no,violator_no,vehicle_id,office_no,vtype,vdate,place,description))
   confirmation = input("confirm data entry. y to confirm, n to exit to menu")
   if confirmation == 'y':
      curs.execute("INSERT INTO ticket VALUES"+str((ticker_no,violator_no,vehicle_id,office_no,vtype,vdate,place,description)))
   else:
      return
   connection.commit()


# def Search2(curs,connection):
#    '''
#    List all violation records received by a person if  the drive 
#    licence_no or sin of a person  is entered.

#    Issues: same as above, how is results expected to be formated?
#    '''
#    curs.execute("SELECT licence_no FROM drive_licence")
#    s2_col_dllicence = set(curs.fetchall()) #list contains all licence_no from drive_licence table
#    real_s2_col_dllicence = set()
#    for i in s2_col_dllicence:
#       real_s2_col_dllicence.add(i[0].strip())

#    curs.execute("SELECT sin FROM people")
#    s2_col_psin = set(curs.fetchall()) # list contains all sin number from people table
#    real_s2_col_psin = set()
#    for i in s2_col_psin:
#       real_s2_col_psin.add(i[0].strip())

#    print(real_s2_col_psin)
#    print('\n\n\n')
#    print(real_s2_col_dllicence)



#    search_input = input("enter sin number or licence number please")

#    if (search_input in real_s2_col_psin):
#       print("searching sin num")
#       execution = "SELECT p.name, dl.licence_no, t.ticket_no, t.vehicle_id, t.vtype, t.vdate, t.place, t.descriptions, tt.fine FROM ticket t, ticket_type tt, people p, drive_licence dl WHERE p.sin = t.violator_no AND p.sin = dl.sin AND tt.vtype = t.vtype and p.sin = '{}'".format(search_input)
#       curs.execute(execution )
#       s2_result = curs.fetchall()
#       print(s2_result)
#       # for r in s2_result:
#       #    print(r)

#    elif (search_input in real_s2_col_dllicence):
#       execution = "SELECT p.name, dl.licence_no, t.ticket_no, t.vehicle_id, t.vtype, t.vdate, t.place, t.descriptions, tt.fine FROM ticket t, ticket_type tt, people p, drive_licence dl WHERE p.sin = t.violator_no AND p.sin = dl.sin AND tt.vtype = t.vtype and dl.licence_no = '{}'".format(search_input)
#       curs.execute(execution )
#       s2_result = curs.fetchall()
#       print(s2_result)
#       # for r in s2_result:
#       #    print(r)

#    else:
#       redo_or_exit = input("No results found. Redo search or exit to search menu? redo/exit")
#       if redo_or_exit =='redo':
#          Search2(curs,connection)
#       else:
#          return 


# def Search3(curs,connection): #the sql query hasn't been built yet. Will get to that eventually, unless you guys there before me
#    '''
#    Print out the vehicle_history, including the number of times that a vehicle has 
#    been changed hand, the average price, and the number of violations it has been 
#    involved by entering the vehicle's serial number.
#    '''
#    curs.execute("SELECT serial_no FROM vehicle")
#    s3_col_vserial = curs.fetchall()

#    search_input = input("Enter vehicle serial number")

#    if search_input in s3_col_vserial:
#       pass
#    else:
#       redo_or_exit = input("No results found. Redo search or exit to search menu? redo/exit")
#       if redo_or_exit =='redo':
#          Search3(curs)
#       elif redo_or_exit == 'exit':
#          return 0

