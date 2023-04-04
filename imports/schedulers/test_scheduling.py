import pytest
import helpers
import subprocess 
from imports.schedulers.scheduling_functions import * 
from imports.schedulers.core_scheduler import *
from imports.schedulers.program_scheduler import *
from database.database import *

#helper function used to grab recently scheduled courses from the database
def get_courses(termA, termB):
    # get a list of fall courses
    db = helpers.check_path(r"database\database.db")
    connection = create_connection(db)
    query = f"SELECT StartDay FROM Lecture L WHERE L.Term = {termA} or L.Term = {termB};"
    
    rows  = []
    try:
        cur = connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    except:
        return None
    
    return rows


# test the basic attributes of the empty starting schedules
@pytest.fixture 
def sched_data():
    # get the initial empty schedules as pandas dataframes
    room_list = get_rooms()
    return {
        'core' : make_empty_scheds(room_list),
        'prgm' : make_empty_scheds(room_list, is_program=True),
        'rooms': room_list       
    }
    
def test_rows(sched_data):
    # check that the starting schedules have the correct number of rows
    assert len((sched_data['core']['lecture']).index) == 19
    assert len((sched_data['prgm']['lecture']).index) == 26
    
def test_cols(sched_data):
    # check that the starting schedules have the correct number of room cols
    sched_rooms = list(sched_data['core']['lecture'].columns) + \
                  list(sched_data['core']['lab'].columns)     + \
                  list(sched_data['core']['online'].columns)
                  
    assert len(sched_data['rooms']) == len(sched_rooms)
    
def test_rooms(sched_data):
    # check that the room names used as column headers are correct
    valid = [r.ID if not r.isLab else f"{r.ID} (LAB)" for r in sched_data['rooms']]
    lec_rooms = list(sched_data['core']['lecture'].columns)
    lab_rooms = list(sched_data['core']['lab'].columns)
    onl_rooms = list(sched_data['core']['online'].columns)
    
    assert all(lec_room in valid for lec_room in lec_rooms)
    assert all(lab_room in valid for lab_room in lab_rooms)
    assert all(onl_room in valid for onl_room in onl_rooms)
    

# test that courses arent scheduled on holidays
@pytest.fixture
def holiday_data():
    return {
        'fall'  : get_sched(1)['holidays'],
        'winter': get_sched(2)['holidays'],
        'spring': get_sched(3)['holidays'],
    }

def test_fall_term(holiday_data):
    holidays = holiday_data['fall']
    courses  = get_courses(1, 3)

    assert len([c for c in courses if c in holidays]) == 0
    
def test_winter_term(holiday_data):
    holidays = holiday_data['winter']
    courses  = get_courses(1, 2)
    
    assert len([c for c in courses if c in holidays]) == 0
    
def test_spring_term(holiday_data):
    holidays = holiday_data['spring']
    courses  = get_courses(2, 3)

    assert len([c for c in courses if c in holidays]) == 0
    
# test that course term hours & new schedules are properly updated
@pytest.fixture 
def course_data():
    test_course = Course("TEST", "TEST", 10, 1, 2, False, False, False, [])
    test_hours  = get_course_hours([test_course])
    test_sched  = pd.DataFrame({"ONLINE": [test_course.ID] * 20})
    
    return {
        'course': test_course,
        'hours' : test_hours,
        'sched' : test_sched,
    }
    
def test_update_hours(course_data):
    course = course_data['course']
    
    new_hours = update_course_hours(course_data['hours'], course_data['sched'])
    
    assert new_hours[course.ID]['remaining'] == 0
    assert new_hours[course.ID]['scheduled'] == course.termHours
    
    
if __name__ == '__main__':
    subprocess.run(["pytest", "-vv"])
    