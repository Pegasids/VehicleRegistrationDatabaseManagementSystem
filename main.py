import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it
#our different modules
from Auto_Transaction import *
from utilities import*
from Search_Functions import *
from Violation_Record import*
from Licence_Registration import*
from Vehicle_Registration import *



#our main application menu
def applications(curs,connection):                                                                        # starts application programs
    exit_code = False
    while exit_code == False:
        print("")
        print("| 'N' New Vehicle Registration    |")
        print("| 'T' Auto Transcation            |")
        print("| 'R' Driver Licence Registration |")
        print("| 'V' Violation Record            |")
        print("| 'S' Search Engine               |")
        print("| 'exitmain' exit                 |")
        print("")
        key = input("Input a key: ")
        if key == 'n' or key == 'N':
            print("")
            VehicleRegistration(curs, connection)
        elif key == 't' or key == 'T':
            print("")
            AutoTransaction(curs, connection)
        elif key == 'r' or key == 'R':
            print("")
            LicenceRegistration(curs, connection)
        elif key == 'v' or key == 'V':
            print("")
            ViolationRecord(curs, connection)
        elif key == 's' or key == 'S':
            print("")
            SearchEngine(curs, connection)
        elif key =='exitmain':
            return
        else:
            print("")
            print("Invalid input, please enter a valid key")


#our search engine menu
def SearchEngine(curs, connection):
    while True:
        print("")
        print("| '1' Search 1                |")
        print("| '2' Search 2                |")
        print("| '3' Search 3                |")
        print("| press any other key to exit |")
        print("")
        key = input("selection please:  ")
        print(key)
        if key == '1':
            print('')
            Search1(curs,connection)
        elif key =='2':
            print('')
            Search2(curs,connection)
        elif key =='3':
            print('')
            Search3(curs,connection)
        else:
            applications(curs,connection)


#this function establishes the connection and then starts up our main menu
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
        Create_all_the_tables(curs,connection)
        Populate_the_shit(curs,connection)

        # Prompt/Start the appliation programs
        applications(curs,connection)

        #----------------------------------------------------------------------------------------------------------------------------

        #close the connection
        curs.close()
        connection.close()

    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)


if __name__ == "__main__":
    project()