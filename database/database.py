#database file - 395 team 8
"""
ref:connection string:  https://www.sqlitetutorial.net/sqlite-python/creating-tables/

Methods for accessing SQL Database.

All methods require an open connection for the conn parameter

For read/delete, pass '%' to fetch/delete all entries in the table.
To read/delete only some entries, pass yourString + '%' to access all entries beginning with yourString.
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
    """
    Creates database connection on passed .db file. 
    Returns connection object or none

    Remember to close opened connections when finished with them!"
    """
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
        #print("opened database successfully")
    except Exception as e:
        print("Error during connection", str(e))

    return conn
def create_table(conn, tableInfo):
   #creates table from passed connection object and SQlite statement 
    try:
        c = conn.cursor()
        c.execute(tableInfo)     
        #print("Table created successfully")
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
        #print("Connection closed")
    except Exception as e:
        print("Error closing database file:", str(e))

    return 

def makeLegion(conn,ProgID, TermID, numStudents):
    legionID= 0
    progTerm = ProgID + str(TermID)
    try:
        queryString = f"Select COUNT(Name) from LEGIONS where Name LIKE '{progTerm}%' "
        cur = conn.cursor()
        cur.execute(queryString)
        legionID = cur.fetchall()
    except Exception as e:
        print("Issues reading from table: ", e)
    if (legionID != 0):
        legionID = int(legionID[0][0]) + 1
    name = ProgID + str(TermID) + "{:02d}".format(legionID)
    legionObj = Legion(ProgID,TermID, legionID, name, numStudents)
    return legionObj

def makeCohort(conn, ProgID, TermID, legions):
    cohortID= 0
    
    try:
        queryString = f"Select COUNT(PID) from COHORT where PID = '{ProgID}' and Term = {TermID}"
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
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
       # print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return legion
def readLegionItem(conn, legionName):
     #reads legion item from DB 
    #parameters:Connection string,  LegionName as string
    rows=[]
    try:
        queryString = f"Select * from LEGIONS where Name like '{legionName}' "
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows

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
            #print(rowString)
            c = conn.cursor()
            c.execute(rowString)
            i= i+1      
        except Exception as e:
            print("Issues inserting into table: ", e)
    return

def addProgramItem_UI(conn, program, course):
    #parameters: passed connection and program ID, and courseID
    try:
        rowString = "INSERT INTO PROGRAMS (ProgID, CourseID) VALUES ('"+ program +"', '"+ course + "')"
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
    except Exception as e:
        print("Issues inserting into table: ", e)
    return

def deleteProgramItem_UI(conn, course):
    #parameters: passed connection and program ID, and courseID
    try:
        rowString = "DELETE FROM PROGRAMS WHERE CourseID='"+ course +"'"
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
    except Exception as e:
        print("Issues deleting from table: ", e)
    return
def readProgramItem(conn, ProgID):
     #reads Program item from DB 
    #parameters:Connection string,  ProgID as a string
    rows= []
    try:
        queryString = f"Select * from PROGRAMS where ProgID like '{ProgID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows
def addClassroomItem(conn, classroom ):
    #add item to table from passed connection and classroom object
    try:
        rowString = "INSERT INTO CLASSROOMS (ClassID , Capacity, IsLab) VALUES (" + classroom.createClassroomItemInfo() + ")"
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        #print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 
def readClassroomItem(conn, ClassID):
     #reads clasroom item from DB 
    #parameters:Connection string, classID as string
    rows = []
    try:
        queryString = f"Select * from CLASSROOMS where ClassID like '{ClassID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows
def deleteClassroomItem(conn, ClassID):
        try:
            queryString = f"delete from CLASSROOMS where ClassID like '{ClassID}'"
            cur = conn.cursor()
            cur.execute(queryString)
            # rows = cur.fetchall()
            # for row in rows:
            #     print(row)
        except Exception as e:
            print("Issues reading from table: ", e)
        return

def addCourseItem(conn,course):
     #add item to table from passed connection and course object
    courseObject = course.createCourseItemInfo()
    #CourseID, title, termHours, duration, isCore, isOnline, isLab, preReq 
    CourseID = courseObject[0]
    title = courseObject[1]
    termHours = courseObject[2]
    term = courseObject[3]
    duration = courseObject[4]
    isCore = courseObject[5]
    isOnline = courseObject[6]
    isLab = courseObject[7]
    preReq = courseObject[8]
    try:
        rowString = f"INSERT INTO COURSES (CourseID, Title, TermHours,Term, Duration, isCore, isOnline, isLab, preReqs) VALUES ('{CourseID}','{title}',{termHours},{term},{duration} ,{isCore}, {isOnline},  {isLab}, '{preReq}')" 
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        #print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return 
def readCourseItem(conn, CourseID):
     #reads Course item from DB 
    #parameters:Connection string, CourseID as string
    rows= []
    try:
        queryString = f"Select * from COURSES where CourseID like '{CourseID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows
def deleteCourseItem(conn, CourseID):
        try:
            queryString = f"delete from COURSES where CourseID like '{CourseID}'"
            cur = conn.cursor()
            cur.execute(queryString)
            # rows = cur.fetchall()
            # for row in rows:
            #     print(row)
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
        rowString = f"INSERT INTO COHORT (PID, Term, CohortID, Legions, Courses) VALUES ('{ProgID}',{TermID},{cohortID},'{legionStr}','{courses}')" 
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        #print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return cohort
def readCohortItem(conn, PID, CohortID):
     #reads cohort item from DB 
    #parameters:Connection string,  CohortID as string
    try:
        queryString = f"Select * from COHORT where CohortID like '{CohortID}' and PID like '{PID}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows
def addLectureItem(conn, lecture):
     #add item to table from passed connection and lecture object
    lectureObject = lecture.createLectureItemInfo()
    CourseID  = lectureObject[0]
    Title     = lectureObject[1]
    CohortID  = lectureObject[2]
    Room      = lectureObject[3]
    TermHours = lectureObject[4]
    Term      = lectureObject[5]
    Duration  = lectureObject[6]
    StartWeek = lectureObject[7]
    StartDay  = lectureObject[8]
    StartTime = lectureObject[9]
    isCore    = 0 if lectureObject[10] == False else 1
    isOnline  = 0 if lectureObject[11] == False else 1
    isLab     = 0 if lectureObject[12] == False else 1
    PreReqs   = lectureObject[13]
    try:
        rowString = f"INSERT INTO LECTURE (CourseID, Title, CohortID, Room, TermHours,Term, Duration, StartWeek, StartDay ,StartTime,isCore,isOnline,isLab, PreReqs) \
            VALUES ('{CourseID}','{Title}','{CohortID}','{Room}' ,{TermHours}, {Term},{Duration}, {StartWeek}, {StartDay}, '{StartTime}',{isCore},{isOnline},{isLab},'{PreReqs}')" 
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        #print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return
def readLectureItem(conn, CourseID, Cohort ):
    #reads lecture item from DB 
    #parameters:Connection string,  courseID and Cohort as strings
    rows =[]
    try:
        queryString = f"Select * from LECTURE where CourseID like '{CourseID}' and CohortID like '{Cohort}'"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows

def readLectureItem_UI(conn, room, day, core):
    #reads lecture item from DB
    #parameters:Connection string,  room as string, week as int
    rows =[]
    try:
        queryString = f"Select * from LECTURE where Room like '{room}' and StartDay like '{day}' and isCore={core}"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows

def readLectureItem_UI_cohorts(conn, cohort, day, core):
    #reads lecture item from DB
    #parameters:Connection string,  room as string, week as int
    rows =[]
    try:
        queryString = f"Select * from LECTURE where CohortID like '{cohort}' and StartDay like '{day}' and isCore={core}"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows

def deleteLectureItem_UI(conn):
    # delete all lecture items
    try:
        queryString = f"DELETE FROM Lecture"
        cur = conn.cursor()
        cur.execute(queryString)
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
def addStudentItem(conn, PID, Term, Count):
    #add item to table from passed connection and student row info
    try:
        rowString = f"INSERT INTO STUDENT (PID , Term, Count) VALUES ('{PID}',{Term},{Count})"
        #print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        #print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
    return 
def readStudentItem(conn, PID, Term):
     #reads student item from DB 
    #parameters:Connection string, PID as string, Term and count as int
    rows = []
    try:
        queryString = f"Select * from STUDENT where PID like '{PID}' and Term like {Term}"
        cur = conn.cursor()
        cur.execute(queryString)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
    except Exception as e:
        print("Issues reading from table: ", e)
    return rows
def deleteStudentItem(conn,  PID, Term):
        try:
            queryString = f"delete from Student where PID like '{PID}' and Term like '{Term}'"
            cur = conn.cursor()
            cur.execute(queryString)
            # rows = cur.fetchall()
            # for row in rows:
            #     print(row)
        except Exception as e:
            print("Issues reading from table: ", e)
        return
##########################End of Read/write helpers ###########################################
