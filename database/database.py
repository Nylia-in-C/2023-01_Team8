#database file - 395 team 8
"""ref:connection string:  https://www.sqlitetutorial.net/sqlite-python/creating-tables/
""" 
import sqlite3
def create_connection(db_file):
    #creates database connection on passed .db file. 
    #returns connection object or none
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
        print("opened database succefully")
    except Exception as e:
        print("Error during connection", str(e))

    return conn

def create_table(conn, tableInfo):
   #creates table from passed connection object and SQlite statement 
    try:
        c = conn.cursor()
        c.execute(tableInfo)     
        print("Table created successfully")
    except Exception as e:
        print(e)

    return 

def close_connection(conn):
    try:
        conn.commit()
        conn.close()
        print("Connection closed")
    except Exception as e:
        print("Error closing database file:", str(e))

    return 

def fillCohortItems(conn, itemInfo, tableName ):
     #add item to table from passed connection object and SQlite statement
    try:
        rowString = "INSERT INTO " + str(tableName) + " (ProgID, TermID, CorhortID, Name, Count) VALUES (" + str(itemInfo) + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
      
        print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 


def createAndFill():
    #main function to build basic database with test cohort data
    
    database = "database.db"  #database.db file path 
    conn = create_connection(database)
    COHORTTableCols = """ CREATE TABLE IF NOT EXISTS COHORT (
                    ProgID VARCHAR(100) NOT NULL,
                    TermID INT NOT NULL,
                    CorhortID INT NOT NULL,
                    Name VARCHAR(100) NOT NULL,
                    Count INT
                ); """
    COURSESTableCols = """ CREATE TABLE IF NOT EXISTS COURSES (
                    CourseID VARCHAR(100) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    termHours INT NOT NULL,
                    duration INT NOT NULL,
                    isCore BIT NOT NULL,
                    isOnline BIT NOT NULL,
                    hasLab BIT NOT NULL
                ); """
    PREREQUISITETableCols = """ CREATE TABLE IF NOT EXISTS PREREQUISITE (
                    PrereqID VARCHAR(100) NOT NULL,
                   CourseID VARCHAR(100) NOT NULL 
                ); """
    
    PROGRAMSTableCols = """ CREATE TABLE IF NOT EXISTS PROGRAMS (
                    ProgID VARCHAR(100) NOT NULL,
                   CourseID VARCHAR(100) NOT NULL 
                ); """
    CLASSROOMSTableCols = """ CREATE TABLE IF NOT EXISTS CLASSROOMS (
                    ClassID VARCHAR(100) NOT NULL,
                    Capacity INT NOT NULL,
                    CorhortID INT NOT NULL,
                    IsLab BIT NOT NULL
                ); """
    cohortItemInfo = """ 'PM', 01, 01, 'PM0101', 6 """
    cohortItemInfo2 = """ 'PM', 01, 02, 'PM0102', 6 """
    cohortItemInfo3 = """ 'PM', 01, 03, 'PM0103', 6 """
    cohortItemInfo4 = """ 'PM', 01, 04, 'PM0103', 6 """
    cohortItemInfo5 = """ 'PM', 02, 05, 'PM0205', 6 """
    cohortItemInfo6 = """ 'PM', 02, 06, 'PM0206', 6 """
    cohortItemInfo7 = """ 'PM', 02, 07, 'PM0207', 6 """
    cohortItemInfo8 = """ 'PM', 02, 08, 'PM0208', 6 """
    cohortItemInfo9 = """ 'BM', 01, 09, 'BM0109', 6 """
    cohortItemInfo10 = """ 'BM', 01, 10, 'BM0110', 6 """
    cohortItemInfo11 = """ 'BM', 01, 11, 'BM0111', 6 """
    cohortItemInfo12 = """ 'BM', 01, 12, 'BM0112', 6 """
    cohortItemInfo13 = """ 'BM', 02, 13, 'BM0213', 6 """
    cohortItemInfo14 = """ 'BM', 02, 14, 'BM0214', 6 """
    cohortItemInfo15 = """ 'BM', 02, 15, 'BM0215', 6 """
    cohortItemInfo16 = """ 'BM', 02, 16, 'BM0216', 6 """
    
    if conn is not None: 
        create_table(conn, COHORTTableCols)
        create_table(conn, COURSESTableCols)
        create_table(conn, PREREQUISITETableCols)
        create_table(conn, PROGRAMSTableCols)
        create_table(conn, CLASSROOMSTableCols) 
        
        fillCohortItems(conn, cohortItemInfo, "COHORT")
        fillCohortItems(conn, cohortItemInfo2, "COHORT")
        fillCohortItems(conn, cohortItemInfo3, "COHORT")
        fillCohortItems(conn, cohortItemInfo4, "COHORT")
        fillCohortItems(conn, cohortItemInfo5, "COHORT")
        fillCohortItems(conn, cohortItemInfo6, "COHORT")
        fillCohortItems(conn, cohortItemInfo7, "COHORT")
        fillCohortItems(conn, cohortItemInfo8, "COHORT")
        fillCohortItems(conn, cohortItemInfo9, "COHORT")
        fillCohortItems(conn, cohortItemInfo10, "COHORT")
        fillCohortItems(conn, cohortItemInfo11, "COHORT")
        fillCohortItems(conn, cohortItemInfo12, "COHORT")
        fillCohortItems(conn, cohortItemInfo13, "COHORT")
        fillCohortItems(conn, cohortItemInfo14, "COHORT")
        fillCohortItems(conn, cohortItemInfo15, "COHORT")
        fillCohortItems(conn, cohortItemInfo16, "COHORT")
 
    else: 
         print("Could not connect to database")
  
    close_connection(conn)
 
    return 

createAndFill()
