# Avery Tan, Canopus Tong, Nathan Nguyen
#Project 1 CMPUT291

import sys
import cx_Oracle
import getpass


def ViolationRecord(curs,connection):
   '''
   This component is used by a police officer to issue a traffic ticket and 
   record the violation. You may assume that all the information about 
   ticket_type has been loaded in the initial database.
   '''

   #collect all ticket numbers to check for primary key constraints
   curs.execute("SELECT ticket_no from ticket")
   col_tick_no__ticket= set(curs.fetchall())
   real_col_tick_no__ticket = set()
   for i in col_tick_no__ticket:
      real_col_tick_no__ticket.add(i[0])


   #collect sin number from people table
   curs.execute("SELECT sin from people")
   col_sin__people = set(curs.fetchall())
   real_col_sin__people = set()
   for i in col_sin__people:
      real_col_sin__people.add(i[0].strip())


   #collect vehicle ids form the vehicle table
   curs.execute("SELECT serial_no from vehicle")
   col_veh_id__vehicle = set(curs.fetchall())
   real_col_veh_id__vehicle = set()
   for i in col_veh_id__vehicle:
      real_col_veh_id__vehicle.add(i[0].strip())


   #collect all ticket types from the ticket_type table
   curs.execute("SELECT vtype from ticket_type")
   col_tick_type__ticket_type = set(curs.fetchall())
   real_col_tick_type__ticket_type = set()
   for i in col_tick_type__ticket_type:
      real_col_tick_type__ticket_type.add(i[0].strip())


   #inpput ticket number and ensure it is unique
   ticker_no = int(input("please enter ticket number"))
   while ticker_no in real_col_tick_no__ticket :
      ticker_no = int(input("ticket number must be unique. reenter, or enter 'exit' to return to main menu"))
      if ticker_no == 'exit':
         return

   #input vehicle id and ensure it is present in the vehicle table
   vehicle_id = input("please enter vehicle id")
   while vehicle_id not in real_col_veh_id__vehicle:
      vehicle_id = input("no such vehicle exists. please reenter vehicle id or type 'exit' to return to menu")
      if vehicle_id == 'exit':
         return

   #choice to give to primary owner or to secondary
   primary_or_generic = input("Add to primary owner? enter y or enter n to manually enter violator id")

   #if no, enter violator number and ensure it is present in the people table
   if primary_or_generic == 'n':
      violator_no = input("please enter violator no")
      while violator_no not in (real_col_sin__people):
         violator_no = input("no such violator exists. please reinput violator_no or type 'exit' to return ot main menu")
         if violator_no == 'exit':
            return
   #this part of the code automatically assigns the violation to the primary owner
   elif primary_or_generic =='y':
      execution = "select owner_id from owner where is_primary_owner = 'y' and vehicle_id = {}".format(vehicle_id)
      curs.execute(execution)
      primary_ownerresult = curs.fetchall()
      list_primary_owner = list()
      for i in primary_ownerresult:
         list_primary_owner.append(i[0].strip())
         violator_no = list_primary_owner[0]
   print("driver ", violator_no, "will be charged! ")


   #enter officer id and ensure he exists in the people table
   office_no = input("please enter officier number")
   while office_no not in real_col_sin__people:
      office_no = input("no such person exists, please reeneter officer number or type 'exit' to return to menu")
      if office_no == 'exit':
         return

   #enter violation type and ensure it exists in the ticket type table
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


