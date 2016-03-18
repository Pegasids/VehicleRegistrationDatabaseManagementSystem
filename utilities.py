


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
   "(licence_no CHAR(15), sin char(15), class VARCHAR(10), photo BLOB,"
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


def Populate(curs,connection):
   '''
   function which populates our database with tuples

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

   print("pass people table")
   ####################################################################################################################################################################


   data_drivelicencetable =  [('100000000000001', '111111111111111','A', '', '01-JAN-2013', '01-JAN-2018'),
                              ('100000000000002', '111111111111112', 'A', '', '02-JAN-2010', '02-FEB-2015'),
                              ('100000000000003', '111111111111113', 'A', '', '03-JAN-2015', '03-JAN-2020'),
                              ('100000000000004', '111111111111114', 'B', "", '12-FEB-2014', '12-FEB-2019'),
                              ('100000000000005', '111111111111115', 'A', '', '15-FEB-2013', '15-OCT-2018'),
                              ('100000000000006', '111111111111116', 'A', '', '13-SEP-2012', '13-DEC-2017'),
                              ('100000000000007', '111111111111117', 'C', '', '03-MAY-2015', '03-JAN-2020'),
                              ('100000000000008', '111111111111118', 'A', '', '03-JAN-2013', '03-JAN-2018'),
                              ('100000000000009', '111111111111119', 'B', '', '02-JAN-2012', '02-JAN-2017'), 
                              ('100000000000010', '111111111111120', 'D', '', '01-JAN-2010', '01-JAN-2015'),
                              ('100000000000011', '111111111111121', 'A', '', '04-JUN-2013', '04-SEP-2018'),
                              ('100000000000012', '111111111111122', 'A', '', '06-JUL-2016', '06-DEC-2021'),
                              ('100000000000013', '111111111111123', 'B', '', '07-DEC-2015', '07-OCT-2020'), 
                              ('100000000000014', '111111111111124', 'A', '', '08-SEP-2014', '08-JAN-2019'),
                              ('100000000000015', '111111111111125', 'D', '', '08-OCT-2012', '08-JAN-2017')]
   curs.bindarraysize = 2
   curs.setinputsizes(15, 15, 10, 10, 10,10) #position 3 is BLOB!! position  position 4 and 5 is DATE!!
   curs.executemany("INSERT INTO drive_licence(licence_no,sin,class,photo,issuing_date, expiring_date) "
                                 "VALUES (:1, :2, :3, :4, :5, :6)", data_drivelicencetable)

   print("pass drive_licence")
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
   print("drivecondition pass")

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



   print("pass restriction")


   data_vehicletypetable = [(10,"SUV"), (11,"Hatchback"), (12,"Sedan"),(13,"Truck"),(14,"Van")]
   curs.bindarraysize = 5
   curs.setinputsizes(int,10)
   curs.executemany("INSERT INTO vehicle_type(type_id, type)"
                                 "VALUES(:1,:2)", data_vehicletypetable)


   print("pass vehicle type")


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



