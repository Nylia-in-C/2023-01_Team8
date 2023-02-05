#database file - 395 team 8
"""ref:connection string:  https://www.sqlitetutorial.net/sqlite-python/creating-tables/
""" 
import sqlite3
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from imports.classes.cohorts import Cohort
from imports.classes.programs import Program
from imports.classes.classrooms import Classroom
from imports.classes.courses import Course


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

def addCohortItem(conn, cohort ):
     #add item to table from passed connection object and SQlite statement
    try:
        rowString = "INSERT INTO COHORT (ProgID, TermID, CorhortID, Name, Count) VALUES (" + cohort.createCohortItemInfo() + ")"
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
       # print("Row added successfully")
    except Exception as e:
        print("Issues inserting into table: ", e)
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
            # print("Row added successfully")
        except Exception as e:
            print("Issues inserting into table: ", e)
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
        rowString = f"INSERT INTO COURSES (CourseID, title, termHours, duration, isCore, isOnline, hasLab, preReqs) VALUES ('{CourseID}','{title}',{termHours},{duration} ,{isCore}, {isOnline},  {hasLab}, '{preReq}')" 
        print(rowString)
        c = conn.cursor()
        c.execute(rowString)
        print("Row added successfully")
    except Exception as e:
            print("Issues inserting into table:", e)
    return 


def createAndFill():
    #main function to build basic database with test cohort data
    
    database = r".\database\database.db"  #database.db file path 
    conn = create_connection(database)    

    if conn is not None: 
        print('success')
        # Dummy = Course('CMSK 1053', 'theTitle', 40, 45, 0,1,0, 'CMSK 1052, CMSK 0157')  
        # #Dummy.printCourse()    
        # addCourseItem(conn,Dummy)

    else: 
         print("Could not connect to database")
  
    close_connection(conn)
 
    return 

createAndFill()
