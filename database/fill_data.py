#Fill database with default objects
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
#from database import *
#import database as database
import database.database as database
#CORE COURSES----------------------------------------------------------------------
# term 1 Professional Communication (PCOM) courses
pcom_0101 = Course("PCOM 0101", "Business Writing I", 35, 1, 1.5, 1, 0, 0, [])
pcom_0105 = Course("PCOM 0105", "Intercultural Communication Skills", 35, 1, 1.5, 1, 0, 0, [])
pcom_0107 = Course("PCOM 0107", "Technical Development I: Microsoft Word, Excel and Power Point", 18,1, 2, 1, 0, 1,[])
cmsk_0233 = Course("CMSK 0233", "MS Project Essentials ", 7,1, 2, 1, 0, 1,[])
cmsk_0235 = Course("CMSK 0235", "MS Visio Essentials",6,1, 2, 1, 0, 1,[])
# term 2 Professional Communication (PCOM) courses
pcom_0102 = Course("PCOM 0102", "Business Writing II", 35, 2, 1.5, 1, 0, 0, [])
pcom_0201 = Course("PCOM 0201", "Fundamentals of Public Speaking", 35, 2, 1.5, 1, 0, 0, [])
pcom_0108 = Course("PCOM 0108", "Technical Development II; Microsoft Word, Excel and Power Point",18,2,2, 1, 0, 1,[])
# term 3 Professional Communication (PCOM) courses
pcom_0202 = Course("PCOM 0202", "Advanced Business Presentation",33,3, 1.5, 1, 0, 0,[])
pcom_0103 = Course("PCOM 0103", "Canadian Workplace Culture",35, 3, 1.5, 1, 0, 0, [])
# pcom_01091 = Course("PCOM 0109 1", "The Job Hunt in Canada lab",8,3, 2, 1, 0, 1,[])
# pcom_01092 = Course("PCOM 0109 2", "The Job Hunt in Canada ",6,3, 2, 1, 0, 0,[])
pcom_0109 = Course("PCOM 0109", "The Job Hunt in Canada",14,3, 2, 1, 0, 0,[])


# term 1 Business Communication (BCOM) courses
pcom_0203 = Course("PCOM 0203", "Effective Professional Writing; Reports, Proposals, Plans and More.",15,1, 2, 1, 0, 0,[])
supr_0751 = Course("SUPR 0751", "Fundamentals of Management and Supervision",7,1, 2, 1, 0, 0,[])
pcom_0204 = Course("PCOM 0204", "Business Persuasion and Research",35,1, 2, 1, 0, 0,[])
cmsk_0237 = Course("CMSK 0237", "Google Suite Essentials",12,1, 2, 1, 1, 0,[])
supr_0837 = Course("SUPR 0837", "Building an Engaged Workforce",7,1, 2, 1, 0, 0,[])
supr_0841 = Course("SUPR 0841", "Change Management Fundamentals",7,1, 2, 1, 0, 0,[])
# term 2 Business Communication (BCOM) courses
supr_0821 = Course("SUPR 0821", "Foundations of Leadership I",7,2, 2, 1, 0, 0,[])
supr_0822 = Course("SUPR 0822", "Foundations of Leadership II",7,2, 2, 1, 0, 0,[])
supr_0718 = Course("SUPR 0718", "Coaching for Performance",7,2, 2, 1, 0, 0,[])
supr_0836 = Course("SUPR 0836", "Hiring for success",7,2, 2, 1, 0, 0,[])
avdm_0199 = Course("AVDM 0199", "Digital Marketing  101",3,2, 2, 1, 1, 0,[])
pcom_0106 = Course("PCOM 0106", "Operations Management",35,2, 2, 1, 0, 0,[])
# term 3 Business Communication (BCOM) courses
pcom_0205 = Course("PCOM 0205", "Small Businesses and Entrepreneurship in Canada",30,3, 3, 1, 0, 0,[])
pcom_tbd = Course("PCOM tbd", "Story Telling (Public Speaking)",21,3, 2, 1, 0, 0,[])
pcom_0207 = Course("PCOM 0207", "Developing Your Emotional Intelligence",6,3, 2, 1, 0, 0,[])
supr_0863 = Course("SUPR 0863", "Design Thinking",7,3, 2, 1, 0, 0,[])
pcom_0206 = Course("PCOM 0206", "Fundamentals of Agile Methdology",6,3, 3, 1, 0, 0,[])
avdm_0260 = Course("AVDM 0260", "WordPress for Web Page Publishing",6,3, 2, 1, 1, 0,[])


# Program Courses------------------------------------------------------------------
# term 1 Project Management (PM) program courses
prdv_0201 = Course("PRDV 0201", "The Basics of Project Management", 21,1, 2, 0, 0, 0, [])
prdv_0202 = Course("PRDV 0202", "Project Scope and Quality", 14,1, 2, 0, 0, 0,[])
prdv_0203 = Course("PRDV 0203", "Fundamentals of Project Planning", 21,1, 2, 0, 0, 0,[])
# term 2 Project Management (PM) program courses
prdv_0204 = Course("PRDV 0204", "Working with Stakeholders", 14,2, 2, 0, 0, 0,[])
prdv_0205 = Course("PRDV 0205", "Leading and Managing a Team", 21,2, 2, 0, 0, 0,[])
pcom_0130 = Course("PCOM 0130", "PM Capstone I", 21,2, 2, 0, 0, 0,[]) #Class should be schedule twice a week half way the term
prdv_0206 = Course("PRDV 0206", "Managing Risk on Projects", 14,2, 2, 0, 0, 0,[])
# term 3 Project Management (PM) program courses
prdv_0207 = Course("PRDV 0207", "Measuring and Reporting on Project Activity", 14,3, 2, 0, 0, 0,[])
pcom_0131 = Course("PCOM 0131", "PM Capstone Project", 39,3, 3, 0, 0, 0,[]) # 13 sessions, 3 hours each


# term 1 Business Analysis (BA) program courses
prdv_0640 = Course("PRDV 0640", "The Basics of Business Analysis", 21,1, 2, 0, 0, 0,[])
prdv_0652 = Course("PRDV 0652", "Business Analysis Planning & Monitoring", 14,1, 2, 0, 0, 0,[])
prdv_0653 = Course("PRDV 0653", "Strategy Analysis", 21,1, 2, 0, 0, 0,[])
prdv_0642 = Course("PRDV 0642", "Elicitation and Collaboration", 14,1, 2, 0, 0, 0,[])
# term 2 Business Analysis (BA) program courses
prdv_0644 = Course("PRDV 0644", "Requirements Analysis & Design Definition", 21,2, 2, 0, 0, 0,[])
prdv_0648 = Course("PRDV 0648", "Requirements Life Cycle Management", 14,2, 2, 0, 0, 0,[])
pcom_0140 = Course("PCOM 0140", "BA Capstone I", 35,2, 2, 0, 0, 0,[])  #Class should be schedule twice a week half way the term
# term 3 Business Analysis (BA) program courses
prdv_0646 = Course("PRDV 0646", "Solution Evaluation", 14,3, 2, 0, 0, 0,[])
pcom_0141 = Course("PCOM 0141", "BA Capstone Project", 39,3, 3, 0, 0, 0,[]) #13 sessions, 3 hours each


# term 1 Book Keeping (BK) program courses
acct_0201 = Course("ACCT 0201", "Bookkeeping Basics", 18,1, 2, 0, 0, 0,[])
acct_0202 = Course("ACCT 0202", "Accounting Basics", 12,1, 2, 0, 0, 0,[])
acct_0203 = Course("ACCT 0203", "Understanding Financial Statements", 12,1, 2, 0, 0, 0,[])
# term 2 Book Keeping (BK) program courses
acct_0206 = Course("ACCT 0206", "Controllership for SMEs", 12,2, 2, 0, 0, 0,[])
acct_0210 = Course("ACCT 0210", "Quickbooks", 28,2, 2, 0, 0, 1,[] )
acct_0211 = Course("ACCT 0211", "SAGE 50 & Data Analytics", 28,2, 2, 0, 0, 1,[])
# term 3 Book Keeping (BK) program courses
acct_0208 = Course("ACCT 0208", "Accounting for Entrepreneurs", 21,3, 2, 0, 0, 1,[])
acct_9901 = Course("ACCT 9901", "Integrated Case Studies in Accounting", 33,3, 2, 0, 0, 1,[])


#term 1 Supply Chain Management & Logistics (GLM) program courses
scmt_0501 = Course("SCMT 0501", "Fundamentals of Supply Chain",21,1,2,0,0,0,[] )
scmt_0502 = Course("SCMT 0502", "Supply Chain Strategy, Design, and Warehousing",21,1,2,0,0,0,[] )
prdv_0304 = Course("PRDV 0304", "Intelligent Supply Chain",15,1,2,0,0,0,[] )
#scmt_9901 = Course("SCMT 9901", "International Transport and Trade",50,1,50,0,1,0,[] ) # (Virtual Course with CIFA; No scheduling required)
#term 2 Supply Chain Management & Logistics (GLM) program courses
scmt_0503 = Course("SCMT 0503", "Supply Chain Dynamics and Risks",15,2,2,0,0,0,[] )
scmt_0504 = Course("SCMT 0504", "Foundations of Inventory, Operations, Planning and Control",21,2,2,0,0,0,[])
#scmt_9902 = Course("SCMT 9902", "Essentials of Freight Forwarding",50,2,50,0,1,0,[] ) # (Virtual Course with CIFA; No scheduling required) 
#term 3 Supply Chain Management & Logistics (GLM) program courses
scmt_0505 = Course("SCMT 0505", "Fundamentals of Supply Chain Analytics",21,3,2,0,0,0,[])
pcom_0151 = Course("PCOM 0151", "Capstone Project",21,3,3,0,0,0,[]) #13 sessions, 3 hours each


#term 1 Digital Experience Design Foundation (DXD) program courses
avdm_0165 = Course("AVDM 0165", "Adobe Photoshop",18,1,2,0,0,1,[])
dxdi_0101 = Course("DXDI 0101", "Digital Experience Design Basics I",24,1,2,0,0,1,[])
dxdi_0102 = Course("DXDI 0102", "Digital Experience Design Basics II",24,1,2,0,0,1,['DXDI 0101'])
#term 2 Digital Experience Design Foundation (DXD) program courses
avdm_0170 = Course("AVDM 0170", "Adobe Illustrator Level I",18,2,2,0,0,1,[])
avdm_0138 = Course("AVDM 0138", "Adobe InDesign Level I",18,2,2,0,0,1,[])
dxdi_0103 = Course("DXDI 0103", "User Interface Design I",24,2,2,0,0,1,['DXDI 0102'])
dxdi_0104 = Course("DXDI 0104", "User Interface Design II",24,2,2,0,0,1,['DXDI 0103'])
#term 3 Digital Experience Design Foundation (DXD) program courses
avdm_0238 = Course("AVDM 0238", "Adobe InDesign Level II",18,3,2,0,0,1,[])
avdm_0270 = Course("AVDM 0270", "Adobe Illustrator Level II",18,3,2,0,0,1,[])
dxdi_9901 = Course("DXDI 9901", "DXD Capstone",45,3,2,0,0,1,[])

#term 1 Full Stack Web Development (FS) program courses
cmsk_0150 = Course("CMSK 0150", "Introduction to Web Development",16,1,2,0,0,1,[])
cmsk_0151 = Course("CMSK 0151", "HTML/CSS Fundamentals",16,1,2,0,0,1,[])
cmsk_0152 = Course("CMSK 0152", "Introduction to JavaScript",16,1,2,0,0,1,['CMSK 0151'])
cmsk_0157 = Course("CMSK 0157", "Introduction to Azure DevOps",16,1,2,0,0,1,[]) #Recommended to run at the same time as CMSK0154
cmsk_0154 = Course("CMSK 0154", "Introduction to C#",16,1,2,0,0,1,[]) #Recommended to run at the same time as CMSK0157
#term 2 Full Stack Web Development (FS) program courses
cmsk_0153 = Course("CMSK 0153", "Introduction to Angular",18,2,2,0,0,1,['CMSK 0151','CMSK 0152','CMSK 0157'])
cmsk_0200 = Course("CMSK 0200", "Advanced C#",16,2,2,0,0,1,['CMSK 0154'])
cmsk_0201 = Course("CMSK 0201", "Entity Framework Core Fundamentals",18,2,2,0,0,1,['CMSK 0154', 'CMSK 0200'])
cmsk_0203 = Course("CMSK 0203", "RESTful Web Services using .NET Core",16,2,2,0,0,1,['CMSK 0201']) #recommend to run the same time as CMSK202
cmsk_0202 = Course("CMSK 0202", "Advanced Angular",18,2,2,0,0,1,[]) #recommend to run the same time as CMSK203
#term 3 Full Stack Web Development (FS) program courses
pcom_0160 = Course("PCOM 0160", "Capstone Project",50,3,2,0,0,1,[])


#-----------------------------------------------------------------------
# default classrooms 
room_533 = Classroom('11-533', 36, 0)
room_534 = Classroom('11-534', 36, 0)
room_560 = Classroom('11-560', 24, 0)
room_562 = Classroom('11-562', 24, 0)
room_564 = Classroom('11-564', 24, 0)
room_458 = Classroom('11-458', 40, 0)
room_430 = Classroom('11-430', 30, 0)
room_320 = Classroom('11-320', 30, 0)
room_532 = Classroom('11-532', 30, 1)
#-----------------------------------------------------------------------
# default programs
#Project Management (PM)
pmObj = Program('PM',["PRDV 0201", "PRDV 0202", "PRDV 0203", "PRDV 0204","PRDV 0205", "PCOM 0130", "PRDV 0206", "PRDV 0207", "PCOM 0131"])
#Business Analysis (BA)
baObj = Program('BA',["PRDV 0640", "PRDV 0652", "PRDV 0653", "PRDV 0642", "PRDV 0644", "PRDV 0648", "PCOM 0140", "PRDV 0646", "PCOM 0141"])
#Book Keeping (BK)
bkObj = Program('BK',["ACCT 0201", "ACCT 0202", "ACCT 0203", "ACCT 0206", "ACCT 0210", "ACCT 0211", "ACCT 0208", "ACCT 9901"])
#Supply Chain Management & Logistics (GLM)
glmObj = Program('GLM',["SCMT 0501","SCMT 0502","PRDV 0304","SCMT 9901","SCMT 0503","SCMT 0504","SCMT 9902","SCMT 0505","PCOM 0151"])
#Digital Experience Design Foundation (DXD)
dxdObj = Program('DXD',["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103", "DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"])
#Full Stack Web Development (FS)
fsObj = Program('FS',["CMSK 0150", "CMSK 0151", "CMSK 0152", "CMSK 0157", "CMSK 0154","CMSK 0153", "CMSK 0200", "CMSK 0201", "CMSK 0203", "CMSK 0202", "PCOM 0160"])
#BCOM
pcomObj = Program('PCOM',["PCOM 0101","PCOM 0105", "PCOM 0107","CMSK 0233","CMSK 0235","PCOM 0102","PCOM 0201","PCOM 0108","PCOM 0202","PCOM 0103","PCOM 0109"])
#PCOM
bcomObj = Program('BCOM',["PCOM 0203","SUPR 0751","PCOM 0204","CMSK 0237","SUPR 0837","SUPR 0841","SUPR 0821","SUPR 0822","SUPR 0718","SUPR 0836","AVDM 0199","PCOM 0106","PCOM 0205","PCOM TBD","PCOM 0207","SUPR 0863","PCOM 0206","AVDM 0260"])
#-----------------------------------------------------------------------
def createDefaultDatabase():
    db = r".\database\database.db"  #database.db file path 
    connection = database.create_connection(db)    
   
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
                    hasLab BIT NOT NULL,
                    PreReqs VARCHAR(200)
                ); """
        COHORTTableCols = """ CREATE TABLE IF NOT EXISTS COHORT (
                    PID VARCHAR(100) NOT NULL,
                    Term INT NOT NULL,
                    CohortID INT NOT NULL,
                    Legions VARCHAR(200) NOT NULL,
                    Courses VARCHAR(200)
                ); """
        STUDENTTableCols = """ CREATE TABLE IF NOT EXISTS STUDENT (
                    PID VARCHAR(100) NOT NULL,
                    Term INT NOT NULL,
                    COUNT INT NOT NULL
                ); """
        # start of add tables********************************************************************
        database.create_table(connection, COHORTTableCols)
        database.create_table(connection, COURSESTableCols)
        database.create_table(connection, LECTURETableCols)
        database.create_table(connection, PROGRAMSTableCols)
        database.create_table(connection, CLASSROOMSTableCols)
        database.create_table(connection, LEGIONSTableCols)  
        database.create_table(connection, STUDENTTableCols)
        # end of add tables**********************************************************************
        
        # start of add courses********************************************************************
        #CORE COURSES----------------------------------------------------------------------
        # term 1 Professional Communication (PCOM) courses
        database.addCourseItem(connection,pcom_0101)
        database.addCourseItem(connection,pcom_0105)
        database.addCourseItem(connection,pcom_0107)
        database.addCourseItem(connection,cmsk_0233)
        database.addCourseItem(connection,cmsk_0235)
        # term 2 Professional Communication (PCOM) courses
        database.addCourseItem(connection,pcom_0102)
        database.addCourseItem(connection,pcom_0201)
        database.addCourseItem(connection,pcom_0108)
        # term 3 Professional Communication (PCOM) courses
        database.addCourseItem(connection,pcom_0202) 
        database.addCourseItem(connection,pcom_0103) 
        #  database.addCourseItem(connection,pcom_01091)
        #  database.addCourseItem(connection,pcom_01092)
        database.addCourseItem(connection,pcom_0109)

       # term 1 Business Communication (BCOM) courses
        database.addCourseItem(connection,pcom_0203)
        database.addCourseItem(connection,supr_0751)
        database.addCourseItem(connection,pcom_0204)
        database.addCourseItem(connection,cmsk_0237)
        database.addCourseItem(connection,supr_0837)
        database.addCourseItem(connection,supr_0841)
        # term 2 Business Communication (BCOM) courses
        database.addCourseItem(connection,supr_0821)
        database.addCourseItem(connection,supr_0822)
        database.addCourseItem(connection,supr_0718)
        database.addCourseItem(connection,supr_0836)
        database.addCourseItem(connection,avdm_0199)
        database.addCourseItem(connection,pcom_0106)
        # term 3 Business Communication (BCOM) courses
        database.addCourseItem(connection,pcom_0205 )
        database.addCourseItem(connection, pcom_tbd)
        database.addCourseItem(connection,pcom_0207 )
        database.addCourseItem(connection,supr_0863 )
        database.addCourseItem(connection,pcom_0206 )
        database.addCourseItem(connection,avdm_0260 )

        # Program Courses------------------------------------------------------------------
        # term 1 Project Management (PM) program courses
        database.addCourseItem(connection,prdv_0201)
        database.addCourseItem(connection,prdv_0202)
        database.addCourseItem(connection,prdv_0203)
        # term 2 Project Management (PM) program courses
        database.addCourseItem(connection,prdv_0204)
        database.addCourseItem(connection,prdv_0205)
        database.addCourseItem(connection,pcom_0130)
        database.addCourseItem(connection,prdv_0206)
        # term 3 Project Management (PM) program courses
        database.addCourseItem(connection,prdv_0207)
        database.addCourseItem(connection,pcom_0131)

        # term 1 Business Analysis (BA) program courses
        database.addCourseItem(connection,prdv_0640)
        database.addCourseItem(connection,prdv_0652)
        database.addCourseItem(connection,prdv_0653)
        database.addCourseItem(connection,prdv_0642)
        # term 2 Business Analysis (BA) program courses
        database.addCourseItem(connection,prdv_0644)
        database.addCourseItem(connection,prdv_0648)
        database.addCourseItem(connection,pcom_0140)
        # term 3 Business Analysis (BA) program courses
        database.addCourseItem(connection,prdv_0646)
        database.addCourseItem(connection,pcom_0141)

        # term 1 Book Keeping (BK) program courses
        database.addCourseItem(connection,acct_0201)
        database.addCourseItem(connection,acct_0202)
        database.addCourseItem(connection,acct_0203)
        # term 2 Book Keeping (BK) program courses
        database.addCourseItem(connection,acct_0206)
        database.addCourseItem(connection,acct_0210)
        database.addCourseItem(connection,acct_0211)
        # term 3 Book Keeping (BK) program courses
        database.addCourseItem(connection,acct_0208 )
        database.addCourseItem(connection,acct_9901 )

        #term 1 Supply Chain Management & Logistics (GLM) program courses
        database.addCourseItem(connection,scmt_0501 )
        database.addCourseItem(connection,scmt_0502 )
        database.addCourseItem(connection,prdv_0304 )
        #scmt_9901
        #term 2 Supply Chain Management & Logistics (GLM) program courses
        database.addCourseItem(connection,scmt_0503 )
        database.addCourseItem(connection,scmt_0504 )
        #scmt_9902
        #term 3 Supply Chain Management & Logistics (GLM) program courses
        database.addCourseItem(connection,scmt_0505) 
        database.addCourseItem(connection,pcom_0151) 

        #term 1 Digital Experience Design Foundation (DXD) program courses
        database.addCourseItem(connection,avdm_0165)
        database.addCourseItem(connection,dxdi_0101)
        database.addCourseItem(connection,dxdi_0102)
        #term 2 Digital Experience Design Foundation (DXD) program courses
        database.addCourseItem(connection,avdm_0170) 
        database.addCourseItem(connection,avdm_0138) 
        database.addCourseItem(connection,dxdi_0103) 
        database.addCourseItem(connection,dxdi_0104) 
        #term 3 Digital Experience Design Foundation (DXD) program courses
        database.addCourseItem(connection,avdm_0238) 
        database.addCourseItem(connection,avdm_0270) 
        database.addCourseItem(connection,dxdi_9901) 

        #term 1 Full Stack Web Development (FS) program courses
        database.addCourseItem(connection,cmsk_0150) 
        database.addCourseItem(connection,cmsk_0151) 
        database.addCourseItem(connection,cmsk_0152) 
        database.addCourseItem(connection,cmsk_0157) 
        database.addCourseItem(connection,cmsk_0154) 
        #term 2 Full Stack Web Development (FS) program courses
        database.addCourseItem(connection,cmsk_0153)
        database.addCourseItem(connection,cmsk_0200) 
        database.addCourseItem(connection,cmsk_0201) 
        database.addCourseItem(connection,cmsk_0203) 
        database.addCourseItem(connection,cmsk_0202) 
        #term 3 Full Stack Web Development (FS) program courses
        database.addCourseItem(connection,pcom_0160)
        # end of add courses**********************************************************************

        # start of add classrooms********************************************************************
        database.addClassroomItem(connection,room_533)
        database.addClassroomItem(connection,room_534)
        database.addClassroomItem(connection,room_560)
        database.addClassroomItem(connection,room_562)
        database.addClassroomItem(connection,room_564)
        database.addClassroomItem(connection,room_458)
        database.addClassroomItem(connection,room_430)
        database.addClassroomItem(connection,room_320)
        database.addClassroomItem(connection,room_532)
        # end of add clasrooms**********************************************************************
                
        # start of add Programs********************************************************************
        database.addProgramItem(connection, pmObj)
        database.addProgramItem(connection, baObj)
        database.addProgramItem(connection, bkObj)
        database.addProgramItem(connection, glmObj)
        database.addProgramItem(connection, dxdObj)
        database.addProgramItem(connection, fsObj)
        database.addProgramItem(connection, pcomObj)
        database.addProgramItem(connection, bcomObj)
       
        # end of add programs**********************************************************************

    else: 
         print("Could not connect to database")
  
    database.close_connection(connection)
 
    return 

#createDefaultDatabase()