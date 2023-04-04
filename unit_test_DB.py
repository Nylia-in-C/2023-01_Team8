import unittest

import os, sys
import sqlite3
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import help_funcs
import fill_data

from imports.classes.legions import Legion
from imports.classes.programs import Program
from imports.classes.programs import Cohort
from imports.classes.classrooms import Classroom
from imports.classes.courses import Course
from imports.classes.courses import Lecture
#from database import *
import database.database as datab

DB = help_funcs.check_path("database\database.db")  #database.db file path 
connection = datab.create_connection(DB)  
TestTableCols = """ CREATE TABLE IF NOT EXISTS TEST (
                        ProgID VARCHAR(100) NOT NULL,
                        COUNT INT NOT NULL
                    ); """
Progobj = Program('PM', ["PRDV 0201", "PRDV 0202", "PRDV 0203", "PRDV 0204", "PRDV 0205", "PCOM 0130", "PRDV 0206", "PRDV 0207", "PCOM 0131"] )
classRmObj = Classroom('11-test', 1,0)
courseObj = Course('courseId', "title",1,2,3,1,1,1,[])
lectObj = Lecture('courseId', "title",1,2,3,1,1,1,[], 'cohort','room',0,0,"8:00")

class TestClass(unittest.TestCase):

    def test_create_connection(self):
        conn = datab.create_connection(DB)
        self.assertIsInstance(conn,sqlite3.Connection)
        self.assertIsNotNone(conn)
    
    # def test_create_table(mock_print):   
    #     datab.create_table(connection, TestTableCols)
    #     #assert mocked_print.mock_calls == [call(""), call()]
    #     mock_print.assert_called_with("Table created successfully")
    def test_makeLegion(self):
        datab.makeLegion(connection, 'TestPID', 0, 999 )
        #legion = self.assertIsInstance(legion,Legion)

    def test_makeCohort(self):
        cohort = datab.makeCohort(connection, 'PM', 0, [])
        self.assertIsInstance(cohort,Cohort)

    def test_addLegionItem(self):
        legion = datab.addLegionItem(connection, 'TestPID', 0, 999)
        self.assertIsInstance(legion,Legion)

    def test_addProgramItem(self):
        with self.assertRaises(Exception):
            try:
                datab.addProgramItem(connection,Progobj)
            except:
                pass
            else:
                raise Exception
    def test_addProgramItem_UI(self):
        with self.assertRaises(Exception):
            try:
                datab.addProgramItem_UI(connection,'PM', 'PCOM101' )
            except:
                pass
            else:
                raise Exception
      
    def test_deleteProgramItem_UI(self):
        with self.assertRaises(Exception):
            try:
                datab.deleteProgramItem_UI(connection,'PCOM101' )
            except:
                pass
            else:
                raise Exception
    def test_addClassroomItem(self):
            with self.assertRaises(Exception):
                try:
                    datab.addClassroomItem(connection,classRmObj )
                except:
                    pass
                else:
                    raise Exception
    def test_deleteClassroomItem(self):
            with self.assertRaises(Exception):
                try:
                    datab.deleteClassroomItem(connection,'11-test')
                except:
                    pass
                else:
                    raise Exception
    
    def test_addCourseItem(self):
        with self.assertRaises(Exception):
            try:
                datab.addCourseItem(connection,courseObj)
            except:
                pass
            else:
                raise Exception
    
    def test_deleteCourseItem(self):
            with self.assertRaises(Exception):
                try:
                    datab.deleteCourseItem(connection,"courseId")
                except:
                    pass
                else:
                    raise Exception 
                 
    def test_addCohortItem(self):
        cohort = datab.addCohortItem(connection, 'PM', 0, [])
        self.assertIsInstance(cohort,Cohort)   
          
    def test_addLectureItem(self):
            with self.assertRaises(Exception):
                try:
                    datab.addLectureItem(connection, lectObj)
                except:
                    pass
                else:
                    raise Exception
    def test_deleteLectureItem_UI(self):
            with self.assertRaises(Exception):
                try:
                    datab.deleteLectureItem_UI(connection)
                except:
                    pass
                else:
                    raise Exception
                
    def test_addStudentItem(self):
            with self.assertRaises(Exception):
                try:
                    datab.addStudentItem(connection, "PID", 1,10)
                except:
                    pass
                else:
                    raise Exception
                
    def test_deleteStudentItem(self):
        with self.assertRaises(Exception):
            try:
                datab.deleteStudentItem(connection, "PID", 1)
            except:
                pass
            else:
                raise Exception
    
                     

unittest.main(exit=False)    
i = 0
tables = ['COHORT','COURSES','LECTURE','PROGRAMS','CLASSROOMS','LEGIONS','STUDENT']
for i in range(len(tables)):
    print('deleting', tables[i])
    datab.delete_table(connection, tables[i])
    i= i+1
datab.close_connection(connection)
fill_data.createDefaultDatabase()