# Avery Tan, Canopus Tong, Nathan Nguyen
#Project 1 CMPUT291


def LicenceRegistration(curs,connection):
   """
   This component is used to record the information needed to issuing a 
   drive licence, including the personal information and a picture for 
   the driver. You may assume that all the image files are stored in a 
   local disk system.

   known issues: Unknown format for DATE and BLOB
   """
   #collecting all sin number in people table
   curs.execute("SELECT sin from people")
   real_col = set()
   list_sin_from_people_table = set(curs.fetchall())
   for i in list_sin_from_people_table:
      real_col.add(i[0].strip())

   #collecting all licence_no from drive_licence table
   curs.execute("SELECT licence_no from drive_licence")
   licence_no__drive_licence = set(curs.fetchall())
   real_licence_no__drive_licence = set()
   for i in licence_no__drive_licence:
      real_licence_no__drive_licence.add(i[0].strip())

   #collecti all sin from drive licence table
   curs.execute("SELECT sin from drive_licence")
   ifalreadylicenced = set()
   list_of_sinfromdrivelicence = curs.fetchall()
   for i in list_of_sinfromdrivelicence:
      ifalreadylicenced.add(i[0].strip())

   #first entry of input asking for the sin number
   sin = input("please enter sin number")


   #determining if sin is empty and thus asks again for data entry of sin
   while sin =='':
      sin = input("empty sin, please enter sin again or type exit to exit to main menu")
      if sin == "exit":
        return

   #determining if the sin number is ALREADY associated with a driver's licence
   while sin in ifalreadylicenced:
      sin = input("this person with the sin already licenced. reenter the sin or type 'exit' to exit")
      if sin == "exit":
         return


   #if sin does not exist in people table, then prepare to either redo or add new entry to people table
   if sin not in real_col:
      choice = input("no sin found, would you like to add new person into people table? y/n")
      if choice =='y':
         #begin data collection for the new people
         p_name = input("please enter people name")
         p_height = input("please enter height")
         p_weight = input("please enter weight")
         p_eyecolor = input("please enter eyecolor")
         p_haircolor = input("please enter haircolor")
         p_addr = input("please enter address")
         p_gender = input("please enter gender. m/f")
         p_birthday = input("please enter birthday")
         confirm = input("confirm entering:({},{},{},{},{},{},{},{},{}) Enter y to confirm, n to return to main menu".format(sin,p_name,p_height,p_weight,p_eyecolor,p_haircolor,p_addr,p_gender,p_birthday))
         values = (sin,p_name,p_height,p_weight,p_eyecolor,p_haircolor,p_addr,p_gender,p_birthday)
         
         #confirm entering the data and give chance to exit to main menu
         if confirm == 'y':
            curs.execute("INSERT INTO people VALUES "+str(values) )
            connection.commit()
         else:
            return

         #continue where we left off, which is entering the remaining details of the drive_licence table
         licence_no = input("please enter license number")
         while licence_no in real_licence_no__drive_licence:
            licence_no = input("license number already exists, enter a unique one please")
         classs = input("please enter class")
         photo = input("please enter photo")
         issuing_date = input("please enter issuing date")
         expiring_date = input("please enter expry date")
         confirm = input("confirm entering({},{},{},{},{},{}) enter y to confirm, n to exit to main menu".format(licence_no,sin,classs,photo,issuing_date,expiring_date))
         

         #confirm entering the data into drive_licence, or we cna exit to main menu
         if confirm == 'y':
            
            #image processing
            f_image = open(photo, 'rb')
            image = f_image.read()
            insert = """insert into drive_licence(licence_no, sin, class, photo,issuing_date, expiring_date)
               values (:licence_no, :sin, :class, :photo, TO_DATE(:issuing_date,'YYYY-MM-DD'), TO_DATE(:expiring_date,'YYYY-MM-DD'))"""
            curs.execute(insert,{'licence_no':licence_no, 'sin':sin, 'class':classs, 'photo':image, 'issuing_date':issuing_date, 'expiring_date':expiring_date})      
            f_image.close()
         
         else: 
            return

      #redo sin number entry or exit to main emnu
      elif choice =='n':
         exit_or_redo = input("would you like to reinput the sin number or exit driver licence registration input? input 'redo' or 'exit'")
         if exit_or_redo == 'exit':
            return
         elif exit_or_redo =='redo':
            LicenceRegistration(curs,connection)
   
   #sin number FOUND! so continue with the entry of our dat ain drive_licence
   else:
      licence_no = input("please enter license number")
      while licence_no in real_licence_no__drive_licence:
         licence_no = input("license must be unique! please reenter")
      classs = input("please enter class")
      photo = input("please enter photo name with extension")
      issuing_date = input("please enter issuing date")
      expiring_date = input("please enter expry date")
      confirm = input("confirm entering({},{},{},{},{},{}) enter y to confirm, n to exit to main menu".format(licence_no,sin,classs,photo,issuing_date,expiring_date))
      if confirm =='y':
         #image_processing
         f_image = open(photo, 'rb')
         image = f_image.read()

         insert = """insert into drive_licence(licence_no, sin, class, photo,issuing_date, expiring_date)
               values (:licence_no, :sin, :class, :photo, TO_DATE(:issuing_date,'YYYY-MM-DD'), TO_DATE(:expiring_date,'YYYY-MM-DD'))"""
         curs.execute(insert,{'licence_no':licence_no, 'sin':sin, 'class':classs, 'photo':image, 'issuing_date':issuing_date, 'expiring_date':expiring_date})      
         f_image.close()
      else:
         return
   connection.commit()
