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
def delete_table(conn, title):
   #deletes table from passed connection object and table title
    tableDrop =  f"DROP TABLE {title}"
    try:
        c = conn.cursor()
        c.execute(tableDrop)     
        print("Table dropped successfully")
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

def makeLegion(conn,ProgID, TermID, numStudents):
    legionID= 0
    progTerm = ProgID + TermID
    try:
        queryString = f"Select COUNT(Name) from LEGIONS where Name LIKE '{progTerm}%' "
        cur = conn.cursor()
        cur.execute(queryString)
        legionID = cur.fetchall()
    except Exception as e:
        print("Issues reading from table: ", e)
    if (legionID != 0):
        legionID = int(legionID[0][0]) + 1
    name = ProgID + TermID + "{:02d}".format(legionID)
    legionObj = Legion(ProgID,TermID, legionID, name, numStudents)
    return legionObj

def makeCohort(conn, ProgID, TermID, legions):
    cohortID= 0
    progTerm = ProgID + TermID
    try:
        queryString = f"Select COUNT(PID) from COHORT where PID = '{ProgID}' and Term = '{TermID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        cohortID = cur.fetchall()
    except Exception as e:
        print("Issues reading from tableS: ", e)
    if (cohortID != 0):
        cohortID = int(cohortID[0][0]) + 1
    cohortID = "{:02d}".format(cohortID)
    cohortObj = Cohort(ProgID, [], legions, TermID, cohortID)
    return cohortObj 

##########################start of Read/write helpers ###########################################
def addLegionItem(conn,ProgID, TermID, numStudents):
     #add item to table from passed connection and Legion object
    legion = makeLegion(conn,ProgID, TermID, numStudents)
    try:
        rowString = "INSERT INTO LEGIONS (ProgID, TermID, LegionID, Name, Count) VALUES (" + legion.createLegionItemInfo() + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
       # print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return legion
def readLegionItem(conn, legionName):
     #reads legion item from DB 
    #parameters:Connection string,  LegionName as string
    try:
        queryString = f"Select * from LEGIONS where Name = '{legionName}' "
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return 
def addProgramItem(conn, program):
    #parameters: passed connection and program object
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
     #reads Program item from DB 
    #parameters:Connection string,  ProgID as a string
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
    #add item to table from passed connection and classroom object
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
     #reads clasroom item from DB 
    #parameters:Connection string, classID as string
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
     #add item to table from passed connection and course object
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
     #reads Course item from DB 
    #parameters:Connection string, CourseID as string
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
def addCohortItem(conn, ProgID, TermID, legions):
     #add item to table from passed connection and cohort object
    cohort = makeCohort(conn, ProgID, TermID, legions)
    cohortObject = cohort.createCohortItemInfo()
    cohortID = cohortObject[2]
    legionStr = cohortObject[3]
    courses = cohortObject[4]
   
    try:
        rowString = f"INSERT INTO COHORT (PID, Term, CohortID, Legions, Courses) VALUES ('{ProgID}','{TermID}',{cohortID},'{legionStr}','{courses}')" 
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return cohort
def readCohortItem(conn, CohortID):
     #reads cohort item from DB 
    #parameters:Connection string,  CohortID as string
    try:
        queryString = f"Select * from COHORT where CohortID = '{CohortID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return
def addLectureItem(conn, lecture):
     #add item to table from passed connection and lecture object
    lectureObject = lecture.createLectureItemInfo()
    CourseID = lectureObject[0]
    Title = lectureObject[1]
    Cohort = lectureObject[2]
    Room = lectureObject[3]
    TermHours = lectureObject[4]
    Duration = lectureObject[5]
    StartWeek = lectureObject[6]
    StartDay = lectureObject[7]
    StartTime = lectureObject[8]
    isCore = lectureObject[9]
    isOnline = lectureObject[10]
    hasLab = lectureObject[11]
    PreReqs = lectureObject[12]
    try:
        rowString = f"INSERT INTO LECTURE (CourseID, Title, Cohort, Room, TermHours,Duration,StartWeek,StartDay,StartTime,isCore,isOnline,hasLab, PreReqs) \
                        VALUES ('{CourseID}','{Title}',{Cohort},'{Room}' ,{TermHours}, {Duration}, {StartWeek}, '{StartDay}', '{StartTime}',{isCore},{isOnline},{hasLab},'{PreReqs}')" 
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return
def readLectureItem(conn, CourseID, Corhort ):
    #reads lecture item from DB 
    #parameters:Connection string,  courseID and Cohort as strings
    try:
        queryString = f"Select * from LECTURE where CourseID = '{CourseID,}' and Corhort = {Corhort}"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return
##########################End of Read/write helpers ###########################################
    
    
def mainTest():
    #main function to connect to database and test helper functions
    database = r".\database\database.db"  #database.db file path 
    connection = create_connection(database)    
   
    if connection is not None: 
       
        #delete_table(connection, "LEGIONS")
        LEGIONSTableCols = """ CREATE TABLE IF NOT EXISTS LEGIONS (
                    ProgID VARCHAR(100) NOT NULL,
                    TermID VARCHAR(100) NOT NULL,
                    legionID INT NOT NULL,
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
                    StartWeek INT NOT NULL,
                    StartDay VARCHAR(100) NOT NULL,
                    StartTime VARCHAR(100) NOT NULL,
                    isCore BIT NOT NULL,
                    isOnline BIT NOT NULL,
                    hasLab BIT NOT NULL,
                    PreReqs VARCHAR(200)
                ); """
        COHORTTableCols = """ CREATE TABLE IF NOT EXISTS COHORT (
                    PID VARCHAR(100) NOT NULL,
                    Term VARCHAR(100) NOT NULL,
                    CohortID INT NOT NULL,
                    Legions VARCHAR(200) NOT NULL,
                    Courses VARCHAR(200)
                ); """
        #Changed CID to PID in Cohort Table creation, since it takes program and it was PID in addCohortItem. If database is complaining drop it and recreate
        
        
        create_table(connection, COHORTTableCols)
        create_table(connection, COURSESTableCols)
        create_table(connection, LECTURETableCols)
        create_table(connection, PROGRAMSTableCols)
        create_table(connection, CLASSROOMSTableCols)
        create_table(connection, LEGIONSTableCols)  

        addLegionItem(connection,'PM', '01', 5)
        addLegionItem(connection,'BA',"01",2)
        addLegionItem(connection,'PM',"02", 0)
        addLegionItem(connection,'PM',"02", 0)
        print(addLegionItem(connection,'PM',"02", 20))

        print(addCohortItem(connection, "PM", "01", ["PM01A, PM01B, PM01C"]))
        print(addCohortItem(connection, "PM", "01", ["PM01D, PM01E, PM01F"]))
        print(addCohortItem(connection, "PM", "02", ["PM01D, PM01E, PM01F"]))

    else: 
         print("Could not connect to database")
  
    close_connection(connection)
 
    return 

mainTest()

 
