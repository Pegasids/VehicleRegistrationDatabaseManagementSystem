# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# File from introduction to cx_oracle



import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

def applications(curs):                                                                        # starts application programs
        exit_code = False
        while exit_code == False:
                print("")
                print("| 'N' New Vehicle Registration    |")
                print("| 'T' Auto Transcation            |")
                print("| 'R' Driver Licence Registration |")
                print("| 'V' Violation Record            |")
                print("| 'S' Search Engine               |")
                print("")
                key = input("Input a key: ")
                if key == 'n' or key == 'N':
                        print("")
                        VehicleRegistration(curs)
                if key == 't' or key == 'T':
                        print("")
                        AutoTransaction(curs)
                if key == 'r' or key == 'R':
                        print("")
                        LicenceRegistration(curs)
                if key == 'v' or key == 'V':
                        print("")
                        ViolationRecord(curs)
                if key == 's' or key == 'S':
                        print("")
                        SearchEngine(curs)
                else:
                        print("")
                        print("Invalid input, please enter a valid key")

def getVRdata(vtrows, vrows, sinrows):                                  # get data from user input and generate data in correct format
#-------Serial Number-----------------------------------------------------------------------------------------------------------
    vrowlst = []    
    for vrow in vrows:
        vrowlst.append(vrow[0].strip())

    print("Vehicle Information")            
    serial_no = input("Serial Number? ").strip()                            # has to be unique
    while serial_no == "" or serial_no in vrowlst:
        serial_no = input("Invalid input / Vehicle already exists in database. Serial Number? ").strip()

#-------Maker-----------------------------------------------------------------------------------------------------------
    maker = input("Maker? ").strip()
    if maker == "": maker = None

#-------Model-----------------------------------------------------------------------------------------------------------
    model = input("Model? ").strip()
    if model == "": model = None

#-------Year-----------------------------------------------------------------------------------------------------------
    year = input("Year? ").strip()
    while not year.isdigit():
        if year == "": 
            year = None
            break
        year = input("Invalid input. Year? ").strip()
        if year == "": 
            year = None
            break
    if year != None: int(year)

#-------Color-----------------------------------------------------------------------------------------------------------
    color = input("Color? ").strip()
    if color == "": color = None

#-------List vehicle_type table-----------------------------------------------------------------------------------------
    print("")
    print("(Type ID) (Type Name)")
    type_id_lst = []
    for vtrow in vtrows:
        type_id_lst.append(str(vtrow[0]))
        print(vtrow[0],". ",vtrow[1], sep='')

#-------Type ID-----------------------------------------------------------------------------------------------------------  
    type_id = input("Type ID? ").strip()                            # has to reference type_id
    while not type_id.isdigit() or type_id not in type_id_lst:
            type_id = input("Invalid input. Type ID? ").strip()
    type_id = int(type_id)

#-------Number of Owner-----------------------------------------------------------------------------------------------------------
    number_of_owner = input("Number of owner? ").strip()
    while not number_of_owner.isdigit():
            number_of_owner = input("Invalid input. Number of owner? ").strip()
    number_of_owner = int(number_of_owner)

#-------Enter Vehicle Infos-----------------------------------------------------------------------------------------------------------  
    oid = []; ipo = []
    for i in range (number_of_owner):           
        print("")

#---------------Owner ID---------------------------------------------------------------------------------------------------
        sin_rowlst = [] 
        for sin in sinrows:
            sin_rowlst.append(sin[0].strip())

        print("Owner", i + 1, "Information")
        owner_id = input("Owner ID? ").strip()                      # has to be unique and references people
        while owner_id in oid or owner_id not in sin_rowlst:
            owner_id = input("Invalid input. Owner ID? ").strip()

#---------------Primary Owner?---------------------------------------------------------------------------------------------------   
        is_primary_owner = input("Primary Owner?(y/n) ").strip()
        while is_primary_owner not in ['y','n','Y','N']:
            is_primary_owner = input("Invalid input. Primary Owner?(y/n) ").strip()
        is_primary_owner = is_primary_owner.lower()

#------------------------------------------------------------------------------------------------------------------
        oid.append(owner_id)                                # Append Owner ID
        ipo.append(is_primary_owner)                            # Append Primary?

#------------------------------------------------------------------------------------------------------------------ 
    vehicle_data = [(serial_no, maker, model, year, color, type_id)]            # generate data in correct format
    owner_data = [(oid[j], serial_no, ipo[j]) for j in range(number_of_owner)]
    #print(vehicle_data, owner_data)
    return vehicle_data, owner_data, number_of_owner

#------------------------------------------------------------------------------------------------------------------

def project():
    
# get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
            user=getpass.getuser()
    
# get password
    pw = getpass.getpass()

# The URL we are connnecting to
    conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'

    try:
        # Establish a connection in Python
        connection = cx_Oracle.connect(conString)

        # create a cursor 
        curs = connection.cursor()

        avery.Create_all_the_tables(curs)
        
        # Prompt/Start the appliation programs
        applications(curs)

        #----------------------------------------------------------------------------------------------------------------------------

        #close the connection
        curs.close()
        connection.close()

    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)

#------------------------------------------New Vehicle Registration-----------------------------------------------------------
def VehicleRegistration(curs):
    # executing queries and get data
    curs.execute("SELECT * from vehicle_type")
    vtrows = curs.fetchall()    
    curs.execute("SELECT serial_no from vehicle")
    vrows = curs.fetchall()     
    curs.execute("SELECT sin from people")
    sinrows = curs.fetchall()   

    # get user data 
    vehicle_data, owner_data, number_of_owner = getVRdata(vtrows,vrows,sinrows)
        
    # get confirmation
    print("")
    confirm = input("Confirm?(y/n) ")
    while confirm not in ['y','n','Y','N']:
        confirm = input("Invalid input. Confirm?(y/n) ").strip()
    if confirm == "y" or confirm == "Y":        
        # Insert values
        curs.bindarraysize = 1
        curs.setinputsizes(15, 20, 20, int, 10, int)
        curs.executemany("INSERT INTO vehicle(serial_no, maker, model, year, color, type_id) "
                    "VALUES (:1, :2, :3, :4, :5, :6)", vehicle_data)
        connection.commit()
            
        curs.bindarraysize = number_of_owner
        curs.setinputsizes(15, 15, 1)
        curs.executemany("INSERT INTO owner(owner_id, vehicle_id, is_primary_owner) "
                    "VALUES (:1, :2, :3)", owner_data)          
        connection.commit()

#-------------------------------------------Auto Transaction----------------------------------------------------
def AutoTransaction(curs):
    # executing queries and get data
        curs.execute("SELECT * from owner")
        orows = curs.fetchall
        curs.execute("SELECT sin from people")
        sinrows = curs.fetchall()
        curs.execute("SELECT serial_no from vehicle")
        vrows = curs.fetchall()
        curs.execute("SELECT transaction_id from auto_sale")
        arows = curs.fetchall()
        
        # get user data
        
        sale_data = getATdata(orows, sinrows, vrows, arows)
        
    # get confirmation
        print("")
        confirm = input("Confirm?(y/n) ")
        while confirm not in ['y','n','Y','N']:
                confirm = input("Invalid input. Confirm?(y/n) ").strip()
        if confirm == "y" or confirm == "Y":
                # Insert values
                curs.bindarraysize = 1
                curs.setinputsizes(int, 15, 15, 15, date, float)
                curs.executemany("INSERT INTO auto_sale(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price) "
                                 "VALUES (:1, :2, :3, :4, :5, :6)", sale_data)

def getATdata(orows, sinrows, vrows, arows):
        # --------------------- Transaction ID ---------------------
        alist = []
        for row in arows:
                alist.append(vrow[0])

        print("Auto Transaction")
        trans_id = input("Transaction ID?").strip()
        while trans_id == "" or trans_id in alist:
                if trans_id == "":
                        trans_id = input("Invalid input. Enter transaction id.\n").strip()
                else:
                        trans_id = input("Transaction id already exists in the database. Enter new transaction id.\n").strip()

        # --------------------- Buyer/Seller ID --------------------
        bsequal = True
        plist = []
        for row in sinrows:
                plist.append(row[0])
        while bsequal == True: 
                seller_id = input("Enter the seller id.\n").strip()

                # change seller and buyer to match test scenarios later
                # for a sale record where the buyer doesn't exist add a new person to the database
                # if the seller is not an owner show an appropriate error message

                # use this for now

                while seller_id == "" or seller_id not in plist:
                        if seller_id == "":
                                seller_id = input("Invalid input. Enter the seller id.\n").strip()
                        else:
                                seller_id = input("Seller does not exist. Enter a new seller id.\n").strip()

                buyer_id = input("Enter the buyer id.").strip()

                while buyer_id == "" or buyer_id not in plist:
                        if buyer_id == "":
                                buyer_id = input("Invalid input. Enter the buyer id.\n").strip()
                        else:
                                buyer_id = input("Seller does not exist. Enter a new buyer id.\n").strip()
        
                if buyer_id == seller_id:
                        print("ID of buyer and seller cannot be the same. Please enter the buyer and seller id again.\n")
                        bsequal = True
                else:
                        bsequal = False
        # ---------------------- Vehicle ID ------------------------
        vsequal = True
        vlist = []
        for row in vrows:
                vlist.append(row[0].)
        while vsequal == True:
                vehicle_id = input("Enter the vehicle id.").strip()
                curs.execute("SELECT * from owner where owner_id = " + seller_id + " and vehicle_id = " + vehicle_id)
                owns = curs.fetchall()
                curs.execute("SELECT * from owner where owner_id = " + seller_id + " and vehicle_id = " + vehicle_id + " and is_primary_owner = 'y' ")
                primary_owner = curs.fetchall()
                if vehicle_id == "":
                        print("Invalid input, try again.").strip()
                elif vehicle_id not in vrows:
                        print("Vehicle does not exist, try again.").strip()
                elif owns == []:
                        print("Vehicle is not owned by the seller, try again.").strip()
                elif primary_owner == []:
                        print("Seller is not the primary owner, try again.").strip()
                else:
                        vsequal = False

        # I'm not exactly sure how to format date and price right now
        # Will do later
        # ------------------------- Date ---------------------------
        date = input("Enter the date of the transaction.\n").strip()

        # ------------------------ Price ---------------------------
        price = input("Enter the sale price of the transaction.\n").strip()

        sale_data = [trans_id, seller_id, buyer_id, vehicle_id, date, price]

        return sale_data

if __name__ == "__main__":

    project()
