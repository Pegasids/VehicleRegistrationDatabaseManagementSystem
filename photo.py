"""
A simple example demonstrating how to insert images into a table.
The table PICTURES used in the example is created with
     create table pictures (
         photo_id integer, 
         title varchar(48), 
         place varchar(48),
         image blob,
         primary key(photo_id)
      )

"""
import cx_Oracle
import getpass

#Retrieve login information
user = input("Username [%s]: " % getpass.getuser())
if not user:
    user=getpass.getuser()
pw = getpass.getpass()
#establish connection
conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
connection = cx_Oracle.connect(conString) 
cursor = connection.cursor()

cursor.execute("create table pictures (photo_id integer, title varchar(10), place varchar(10), image blob, primary key (photo_id) )")
# information for the new row
pid=101
title="Window"
place="Utah" 
#Load image into memory from local file 
#(Assumes a file by this name exists in the directory you are running from)
f_image  = open('sample.jpg','rb')
image  = f_image.read()

# prepare memory for operation parameters
cursor.setinputsizes(image=cx_Oracle.BLOB)
 
insert = """insert into pictures (photo_id, title, place, image)
   values (:photo_id, :title, :place, :image)"""
cursor.execute(insert,{'photo_id':pid, 'title':title,
                           'place':place, 'image':image})
connection.commit()
# Housekeeping...
f_image.close()
cursor.close()
connection.close()

"""
To check that the picture was inserted open sqldeveloper double click the pictures table and go to the data tab. You should see one row with the image as (blob). If you double-click the blob you will see a button marked "...", click that button and select view as image. 
"""