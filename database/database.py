#database file - 395 team 8
"""ref:connection string:  https://www.sqlitetutorial.net/sqlite-python/creating-tables/
""" 
import sqlite3
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from imports.classes.legions import Legion
from imports.classes.programs import Program
from imports.classes.programs import Cohort
from imports.classes.classrooms import Classroom
from imports.classes.courses import Course
from imports.classes.courses import Lecture


def create_connection(db_file):
    #creates database connection on passed .db file. 
    #returns connection object or none
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
        print("opened database successfully")
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

def addLegionItem(conn, legion ):
     #add item to table from passed connection object and SQlite statement
    try:
        rowString = "INSERT INTO LEGION (ProgID, TermID, CorhortID, Name, Count) VALUES (" + legion.createLegionItemInfo() + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
       # print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 
def readLegionItem(conn, legionName):
    try:
        queryString = f"Select * from LEGION where Name = '{legionName}' "
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return 
    
def addProgramItem(conn, program):
    #adds programID and CourseID into table, one courseID per row
    programObject = program.createProgramItemInfo()
    programID = programObject[0]
    courseList = programObject[1]
    i = 0
    for course in courseList:
        try:
            rowString = "INSERT INTO PROGRAMS (ProgID, CourseID) VALUES ('"+ programID +"', '"+ courseList[i] + "')"
            print(rowString)
            c = conn.cursor()
            c.execute(rowString)
            i= i+1      
        except Exception as e:
            print("Issues inserting into table: ", e)
    return 

def readProgramItem(conn, ProgID):
    try:
        queryString = f"Select * from PROGRAMS where ProgID = '{ProgID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return 

def addClassroomItem(conn, classroom ):
     #add item to table from passed connection object and SQlite statement
    try:
        rowString = "INSERT INTO CLASSROOMS (ClassID , Capacity, IsLab) VALUES (" + classroom.createClassroomItemInfo() + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 
def readClassroomItem(conn, ClassID):
    try:
        queryString = f"Select * from CLASSROOMS where ClassID = '{ClassID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return 

def addCourseItem(conn,course):
    courseObject = course.createCourseItemInfo()
    #CourseID, title, termHours, duration, isCore, isOnline, hasLab, preReq 
    CourseID = courseObject[0]
    title = courseObject[1]
    termHours = courseObject[2]
    duration = courseObject[3]
    isCore = courseObject[4]
    isOnline = courseObject[5]
    hasLab = courseObject[6]
    preReq = courseObject[7]
    try:
        rowString = f"INSERT INTO COURSES (CourseID, Title, TermHours, Duration, isCore, isOnline, hasLab, preReqs) VALUES ('{CourseID}','{title}',{termHours},{duration} ,{isCore}, {isOnline},  {hasLab}, '{preReq}')" 
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return 
def readCourseItem(conn, CourseID):
    try:
        queryString = f"Select * from COURSES where CourseID = '{CourseID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return
def addCohortItem(conn,cohort):
    cohortObject = cohort.createCohortItemInfo()
    cid = cohortObject[0]
    term = cohortObject[1]
    cohortID = cohortObject[2]
    legionStr = cohortObject[3]
    courses = cohortObject[4]
   
    try:
        rowString = f"INSERT INTO COHORT (CID, Term, CohortID, Legions, Courses) VALUES ('{cid}','{term}',{cohortID},'{legionStr}' ,'{courses}')" 
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return
def readCohortItem(conn, cid):
    try:
        queryString = f"Select * from COHORT where CID = '{cid}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return
     
def mainTest():
    #main function to connect to database and test helper functions
    
    database = r".\database\database.db"  #database.db file path 
    conn = create_connection(database)    

    if conn is not None: 
        print('success')
        LEGIONSTableCols = """ CREATE TABLE IF NOT EXISTS LEGIONS (
                    ProgID VARCHAR(100) NOT NULL,
                    TermID INT NOT NULL,
                    CorhortID INT NOT NULL,
                    Name VARCHAR(100) NOT NULL,
                    Count INT
                ); """
        COURSESTableCols = """ CREATE TABLE IF NOT EXISTS COURSES (
                    CourseID VARCHAR(100) NOT NULL,
                    Title VARCHAR(100) NOT NULL,
                    TermHours INT NOT NULL,
                    Duration INT NOT NULL,
                    isCore BIT NOT NULL,
                    isOnline BIT NOT NULL,
                    hasLab BIT NOT NULL, 
                    PreReqs VARCHAR(200)
                ); """ 
        PROGRAMSTableCols = """ CREATE TABLE IF NOT EXISTS PROGRAMS (
                    ProgID VARCHAR(100) NOT NULL,
                   CourseID VARCHAR(100) NOT NULL 
                ); """
        CLASSROOMSTableCols = """ CREATE TABLE IF NOT EXISTS CLASSROOMS (
                    ClassID VARCHAR(100) NOT NULL,
                    Capacity INT NOT NULL,
                    IsLab BIT NOT NULL
                ); """
        LECTURETableCols = """ CREATE TABLE IF NOT EXISTS LECTURE (
                    CourseID VARCHAR(100) NOT NULL,
                    Title VARCHAR(100) NOT NULL,
                    Corhort VARCHAR(100) NOT NULL,
                    Room VARCHAR(100) NOT NULL,
                    TermHours INT NOT NULL,
                    Duration INT NOT NULL, 
                    StartWeek VARCHAR(100) NOT NULL,
                    StartDay VARCHAR(100) NOT NULL,
                    StartTime VARCHAR(100) NOT NULL,
                    isCore BIT NOT NULL,
                    isOnline BIT NOT NULL,
                    hasLab BIT NOT NULL,
                    PreReqs VARCHAR(200)
                ); """
        COHORTTableCols = """ CREATE TABLE IF NOT EXISTS COHORT (
                    CID VARCHAR(100) NOT NULL,
                    Term VARCHAR(100) NOT NULL,
                    CohortID INT NOT NULL,
                    Legions VARCHAR(200) NOT NULL,
                    Courses VARCHAR(200)
                ); """
        
        create_table(conn, COHORTTableCols)
        create_table(conn, COURSESTableCols)
        create_table(conn, LECTURETableCols)
        create_table(conn, PROGRAMSTableCols)
        create_table(conn, CLASSROOMSTableCols)
        create_table(conn, LEGIONSTableCols)   

        # courseDummy = Course('CMSK 1053', 'testname',100,23,1,1,0,["CMSK 1052", "CMSK 0157"])
        # addCourseItem(conn, courseDummy)
        # programDummy = Program('FS',["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103", "DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"])
        # addProgramItem(conn, programDummy)
        #CohortDummy = Cohort('FS',["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103", "DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"], ["11","10","9"] , '01', 0)  
        #addCohortItem(conn,CohortDummy)
        readCohortItem(conn, 'FS')
    else: 
         print("Could not connect to database")
  
    close_connection(conn)
 
    return 

mainTest()
