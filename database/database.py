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
##########################start of Read/write helpers ###########################################
def addLegionItem(conn, legion ):
     #add item to table from passed connection and Legion object
    try:
        rowString = "INSERT INTO LEGIONS (ProgID, TermID, CorhortID, Name, Count) VALUES (" + legion.createLegionItemInfo() + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
       # print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 
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
def addCohortItem(conn,cohort):
     #add item to table from passed connection and cohort object
    cohortObject = cohort.createCohortItemInfo()
    cid = cohortObject[0]
    term = cohortObject[1]
    cohortID = cohortObject[2]
    legionStr = cohortObject[3]
    courses = cohortObject[4]
   
    try:
        rowString = f"INSERT INTO COHORT (CID, Term, CohortID, Legions, Courses) VALUES ('{cid}','{term}',{cohortID},'{legionStr}','{courses}')" 
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return
def readCohortItem(conn, cid):
     #reads cohort item from DB 
    #parameters:Connection string,  CID as string
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

def LegionsCount(conn,ProgID, TermID):
    try:
        queryString = f"Select COUNT(*) from LEGIONS where ProgID = '{ProgID,}' and TermID = {TermID}"
        cur = conn.cursor()
        cur.execute(queryString)
        count = cur.fetchall()
        
    except Exception as e:
        print("Issues reading from table: ", e)

    return count


def mainTest():
    #main function to connect to database and test helper functions
    
    database = r".\database\database.db"  #database.db file path 
    conn = create_connection(database)    

    if conn is not None: 
        print('success')
      
        LEGIONSTableCols = """ CREATE TABLE IF NOT EXISTS LEGIONS (
                    ProgID VARCHAR(100) NOT NULL,
                    TermID VARCHAR(100) NOT NULL,
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
                    StartWeek INT NOT NULL,
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
        # CohortDummy = Cohort('FS',["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103", "DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"], ["11","10","9"] , '01', 0)  
        # addCohortItem(conn,CohortDummy)
        # readCohortItem(conn, 'FS')
        # LectureDummy = Lecture('AVDM 0165',"Test title", "cohort","room", 0, 1, 2,"startDay","start time", 1,0,1, ["CMSK 1052", "CMSK 0157"])  
        # addLectureItem(conn,LectureDummy)
        Legion1 = Legion('PM',"01", 0) 
        Legion2 = Legion('BA',"01",2)  
        Legion3 = Legion('PM',"01", 0)  
        Legion4 = Legion('PM',"02", 0)  
        Legion5 = Legion('PM',"01", 0)  
        Legion6 = Legion('PM',"02", 0)   
        addLegionItem(conn,Legion1)
        addLegionItem(conn,Legion2)
        addLegionItem(conn,Legion3)
        addLegionItem(conn,Legion4)
        addLegionItem(conn,Legion5)
        addLegionItem(conn,Legion6)
    else: 
         print("Could not connect to database")
  
    close_connection(conn)
 
    return 

mainTest()
