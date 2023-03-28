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
#from database import *
import database as database

def mainTest():
    #main function to connect to database and test helper functions
    database = r".\database\database.db"  #database.db file path 
    connection = database.create_connection(database)    
   
    if connection is not None: 
       
        database.delete_table(connection, "LECTURE")
        LEGIONSTableCols = """ CREATE TABLE IF NOT EXISTS LEGIONS (
                    ProgID VARCHAR(100) NOT NULL,
                    TermID INT NOT NULL,
                    legionID INT NOT NULL,
                    Name VARCHAR(100) NOT NULL,
                    Count INT
                ); """
        COURSESTableCols = """ CREATE TABLE IF NOT EXISTS COURSES (
                    CourseID VARCHAR(100) NOT NULL,
                    Title VARCHAR(100) NOT NULL,
                    TermHours INT NOT NULL,
                    Term INT NOT NULL,
                    Duration INT NOT NULL,
                    isCore BIT NOT NULL,
                    isOnline BIT NOT NULL,
                    isLab BIT NOT NULL, 
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
                    CohortID VARCHAR(100) NOT NULL,
                    Room VARCHAR(100) NOT NULL,
                    TermHours INT NOT NULL,
                    Term INT NOl NULL,
                    Duration INT NOT NULL, 
                    StartWeek INT NOT NULL,
                    StartDay INT NOT NULL,
                    StartTime VARCHAR(100) NOT NULL,
                    isCore BIT NOT NULL,
                    isOnline BIT NOT NULL,
                    isLab BIT NOT NULL,
                    PreReqs VARCHAR(200)
                ); """
        COHORTTableCols = """ CREATE TABLE IF NOT EXISTS COHORT (
                    PID VARCHAR(100) NOT NULL,
                    Term INT NOT NULL,
                    CohortID INT NOT NULL,
                    Legions VARCHAR(200) NOT NULL,
                    Courses VARCHAR(200)
                ); """
     
        
      
        database.create_table(connection, COHORTTableCols)
        database.create_table(connection, COURSESTableCols)
        database.create_table(connection, LECTURETableCols)
        database.create_table(connection, PROGRAMSTableCols)
        database.create_table(connection, CLASSROOMSTableCols)
        database.create_table(connection, LEGIONSTableCols)  

        database.addLegionItem(connection,'PM', '01', 5)
        database.addLegionItem(connection,'BA',"01",2)
        database.addLegionItem(connection,'PM',"02", 0)
        database.addLegionItem(connection,'PM',"02", 0)
        print(database.addLegionItem(connection,'PM',"02", 20))

        database.addCohortItem(connection, "PM", "01", ["PM01A. PM01B. PM01C"])
        database.addCohortItem(connection, "PM", "01", ["PM01D. PM01E. PM01F"])
        database.addCohortItem(connection, "PM", "02", ["PM01D. PM01E. PM01F"])

        val = database.readCohortItem(connection,'PM', '1' )
        print('VALUE', val)
        lectureObj = Lecture('CourseID', 'title', 20, 100, 3, 1,0,0, ['preReq', 'preReq'],'cohortID','room',13, 5,'startTime')
        database.addLectureItem(connection, lectureObj)
        val = database.readLectureItem(connection, 'CourseID', 'cohortID' )
        print('VALUE', val)
        classroomObj = Classroom('ClassroomID101', 100,1)
        database.addClassroomItem(connection, classroomObj)
        val = database.readClassroomItem(connection,'ClassroomID')
        print('VALUE', val)
        database.addLegionItem(connection,'ProgID', 2, 100)
        val = database.readLegionItem(connection,'PM0101')
        print('VALUE', val)
        programObj = Program('DXD', ["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103","DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"] )
        database.addProgramItem(connection, programObj)
        val = database.readProgramItem(connection,'%')
        print('VALUE', val)
        courseObj = Course('CMSK 1053', 'title', 100,3, 101,1,0,0,["CMSK 1052", "CMSK 0157"])
        database.addCourseItem(connection, courseObj)
        val = database.readCourseItem(connection,'CMSK 1053')
        print('VALUE', val)
        database.deleteClassroomItem(connection,'%')

    else: 
         print("Could not connect to database")
  
    database.close_connection(connection)
 
    return 


mainTest()