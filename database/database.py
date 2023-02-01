#database file - 395 team 8
"""ref:connection string:  https://www.sqlitetutorial.net/sqlite-python/creating-tables/
""" 
import sqlite3
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from imports.classes.cohorts import Cohort

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

def fillCohortItems(conn, cohort, tableName ):
     #add item to table from passed connection object and SQlite statement
    try:
        rowString = "INSERT INTO " + str(tableName) + " (ProgID, TermID, CorhortID, Name, Count) VALUES (" + cohort.createItemInfo() + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
      
        print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 


def createAndFill():
    #main function to build basic database with test cohort data
    
    database = "2023-01_Team8\database\database.db"  #database.db file path 
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
    cohort1  = Cohort ('PM', '01', 5)
    cohort2  = Cohort ('PM', '01', 6)
    cohort3  = Cohort ('PM', '01', 6)
    cohort4  = Cohort ('PM', '01', 6)
    cohort5  = Cohort ('PM', '02', 6)
    cohort6  = Cohort ('PM', '02', 6)
    cohort7  = Cohort ('PM', '02', 6)
    cohort8  = Cohort ('PM', '02', 6)
    cohort9  = Cohort ('BA', '01', 6)
    cohort12 = Cohort ('BA', '01', 6)
    cohort10 = Cohort ('BA', '01', 6)
    cohort13 = Cohort ('BA', '02', 6)
    cohort14 = Cohort ('BA', '02', 6)
    cohort11 = Cohort ('BA', '01', 6)
    cohort15 = Cohort ('BA', '02', 6)
    cohort16 = Cohort ('BA', '02', 6)
    
    if conn is not None: 
        create_table(conn, COHORTTableCols)
        create_table(conn, COURSESTableCols)
        create_table(conn, PREREQUISITETableCols)
        create_table(conn, PROGRAMSTableCols)
        create_table(conn, CLASSROOMSTableCols) 
        
        fillCohortItems(conn, cohort1,  "COHORT")
        fillCohortItems(conn, cohort2,  "COHORT")
        fillCohortItems(conn, cohort3,  "COHORT")
        fillCohortItems(conn, cohort4,  "COHORT")
        fillCohortItems(conn, cohort5,  "COHORT")
        fillCohortItems(conn, cohort6,  "COHORT")
        fillCohortItems(conn, cohort7,  "COHORT")
        fillCohortItems(conn, cohort8,  "COHORT")
        fillCohortItems(conn, cohort9,  "COHORT")
        fillCohortItems(conn, cohort10, "COHORT")
        fillCohortItems(conn, cohort11, "COHORT")
        fillCohortItems(conn, cohort12, "COHORT")
        fillCohortItems(conn, cohort13, "COHORT")
        fillCohortItems(conn, cohort14, "COHORT")
        fillCohortItems(conn, cohort15, "COHORT")
        fillCohortItems(conn, cohort16, "COHORT")
 
    else: 
         print("Could not connect to database")
  
    close_connection(conn)
 
    return 

createAndFill()
