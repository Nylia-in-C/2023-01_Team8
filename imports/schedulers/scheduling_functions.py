import os, sys
import math
import datetime
import pandas as pd
import numpy as np
import holidays
import static_frame as sf

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from imports.classes.courses import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
from imports.fillClassrooms import *
from database.database import *
import string
from itertools import permutations, cycle, chain
from collections import defaultdict
from typing import *
from pprint import pprint



#===================== TODOs (in no particular order) ==========================       


# TODO: when updating schedule, check if any courses are scheduled for more than their remaining hours
#       if so, remove some blocks

# TODO: find way to check if avdm should be scheduled (i.e. 2 days away from end date)


day = 1
week = 1
lecture_objs = []
# ==============================================================================


#=========================== INITIAL DATA RETREIVAL ============================
def get_courses(prog: str, term: int) -> List[Course]:
    ''' fetch all courses for a given program & term from the database '''
    db = r".\database\database.db"  # database.db file path
    connection = create_connection(db)

    query = f"SELECT C.* FROM \
              Courses C JOIN Programs P ON C.CourseID = P.CourseID WHERE \
              P.ProgID = '{prog}' AND C.Term = {term};"

    try:
        cur = connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    except:
        print("unable to retrieve core courses from database")
        return

    close_connection(connection)

    # convert strings from the database into Course objects
    courses = []
    for row in rows:
        row = list(row)
        # convert 0/1 to booleans
        for i in range(5, 8):
            if   row[i] == 0: row[i] = False
            elif row[i] == 1: row[i] = True

        courses.append( Course(*row) )

    return courses
    
def get_rooms() -> List[Classroom]:
    ''' fetch all non-ghost classrooms from the database'''
    db = r".\database\database.db"  # database.db file path
    connection = create_connection(db)

    query = f"SELECT * FROM Classrooms C WHERE C.ClassID NOT LIKE 'ghost%';"

    try:
        cur = connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    except:
        print("unable to retrieve classrooms from database")

    close_connection(connection)

    rooms = []
    for row in rows:
        row = list(row)
        isLab = False
        if int(row[2]) == 1:
            isLab = True
        rooms.append(Classroom(row[0], int(row[1]), isLab))

    return rooms

def get_cohort_counts(term: int) -> Dict[str, int]:
    ''' 
    call `fillClassrooms` to get a breakdown of all cohorts, then return a 
    cohort count for each program/term
    '''
    cohort_dict = fillClassrooms(term)
    counts = {}
    for program, cohorts in cohort_dict.items():
        counts[program] = len(cohorts)
    
    return counts
#===============================================================================


#============================ HELPER FUNCTIONS =================================
def create_empty_schedule(room_list: List[Classroom]) -> pd.DataFrame:
    '''
    make an empty pandas dataframe to represent the schedule for a single day. 
    Column headers are room numbers & row indexes are times (half hour increments)
    '''
    
    times = [datetime.time(i, j).strftime("%H:%M")
             for i in range(8, 17) for j in [0, 30]]
    times.append(datetime.time(17, 0).strftime("%H:%M"))

    sched = pd.DataFrame(index=times)
    
    for room in room_list:
        if not room.isLab:
            sched[room.ID] = [""] * 19
        else:
            sched[f"{room.ID} (LAB)"] = [""] * 19

    return sched

def get_course_hours(courses: List[Course]) -> Dict[str, int]:
    '''
    Create a dictionary that will keep track of how many hours
    a given course has, and how many hours it has left. 
    '''
    hours = {}

    for course in courses:
        hours[course.ID] = {
            'required': course.termHours,
            'remaining': course.termHours,
            'scheduled': 0,
        }

    return hours

def update_course_hours(course_hours: Dict[str, int], prev_schedule: pd.DataFrame) -> Dict[str, str]:
    '''
    Use the previous day's schedule to update the remaining hours for each course
    '''
    # dont update the same course twice
    seen = set()

    # get number of hours for each course on the schedule
    for room in prev_schedule.columns:
        courses = prev_schedule[room].tolist()
        for course in courses:
            if (course == ""):
                continue

            # remove cohort identifier from non-online courses
            course_name = course[:-2] if room != 'ONLINE' else course

            if course_name in seen:
                continue

            seen.add(course_name)
            
            scheduled_hours = (courses.count(course)) * 0.5
                
            course_hours[course_name]['scheduled'] += scheduled_hours
            course_hours[course_name]['remaining'] -= scheduled_hours

    return course_hours

def update_schedule(course_hours: Dict[str, int], prev_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the previous day's schedule and the course hours dict. If any courses
    have met their term hour requirements, they are removed and replaced with empty strings
    '''

    # courses that have met their required hours should be removed
    finished = [course_id for course_id in course_hours if
                        course_hours[course_id]['remaining'] <= 0]

    for time in prev_sched.index:
        for room in prev_sched.columns:
            
            course_no_ID = prev_sched.loc[time, room][:-2]
            course_w_ID  = prev_sched.loc[time, room]

            if course_no_ID in finished or course_w_ID in finished:
                
                # empty strings indicate an open time slot in the schedule
                prev_sched.loc[time, room] = "" 

    return prev_sched

def filter_courses(courses: List[Course], sched: pd.DataFrame, 
                   course_hours: Dict[str, int]) -> List[Course]:
    '''
    Take a list of courses and filter out ones that have already been added to 
    the schedule or have already met their term hour requirements. Sort the list
    of courses in descending order of total term hours before returning it
    '''
    
    # TODO: add checks for edge cases 
    # (e.g. certain courses have to be start on a certain day of the term)
    
    # given course list should only contain a single type of course
    # (online courses dont include cohort IDs)
    if all(c.isOnline for c in courses):
        scheduled = [c for c in sched.values.flatten()]
    else:
        scheduled = [c[:-2] for c in sched.values.flatten()]
    
    valid = [c for c in courses if c.ID not in scheduled 
             and course_hours[c.ID]['remaining'] > 0]
    
    valid.sort(key=lambda x: x.termHours, reverse=True)
    
    return valid

def get_time_slot_count(course: Course, course_hours: Dict[str, int]) -> int:
    '''
    Checks a given courses duration, and how many term hours it has left and
    returns the number of half-hour blocks it should be scheduled for
    '''
    hours_left = course_hours[course.ID]['remaining']
    
    if (hours_left >= course.duration):
        return int(course.duration // 0.5)
    else:
        return math.ceil(hours_left / 0.5)

def get_available_times(sched: pd.DataFrame,
                        blocks: int, cohorts: int) -> Dict[str, List[int]]:
    '''
    Takes the current schedule, the number of half-hour blocks a given course 
    will take up, and the number of cohorts needed. Returns a dictionary mapping
    room names to a list of available start times (indexes). If there arent enough
    available times for all cohorts, returns an empty dict
    '''
    available = defaultdict(list)
    required_gap = [""] * blocks

    # use a sliding window to find an available time & keep track of how many you find
    left = 0
    right = blocks
    count = 0

    # keep track of when the last added course ends to prevent overlapping courses
    prev_course_end = -1

    # iterate room by room, starting at 8:00. Move to the next time period when
    # we reach the last room
    for room in cycle(sched.columns.tolist()):

        # at the last room & the last time slot
        if room == list(sched.columns)[-1] and right >= 20:
            break

        # found an open time gap
        if list(sched[room][left:right]) == required_gap:
            # check if adding current course will overlap with the previous one
            if (left >= prev_course_end):
                available[room].append(left)
                prev_course_end = right
                count += 1

        # reached the last room, move to the next starting time
        if room == list(sched.columns)[-1]:
            left += 1
            right += 1

    # return empty dict if there aren't enough available times for all cohorts
    if count < cohorts:
        return {}

    return available

def get_valid_cohorts(invalid_courses: List[str], start: int, end: int,
                      cohorts: List[str], curr_room: str, sched: pd.DataFrame) -> Set[str]:
    '''
    Given a potential start time and duration for a course, returns a set of 
    unique cohort IDs that can be used (prevent scheduling conflicts). 
    '''
    # list of all times the course will occupy
    occupied_times = [t for t in range(start, end)]
    # get dict of rooms mapped to the row indexes of any incompatible courses
    # scheduled at any of the time slots the new course might occupy
    matching_courses = {}
    for room in sched.columns:

        if room == curr_room:
            continue

        matches = sched[room].apply(
            lambda x: any([c in str(x[:-2]) for c in invalid_courses])
        )
        times = list(matches[matches].index.values)
        overlap = [t for t in times if times.index(t) in occupied_times]

        matching_courses[room] = overlap

    invalid_cohorts = set()
    # for each occupied time for the new course, add the unavailable cohorts to a set
    for room, times in matching_courses.items():
        for time in times:

            invalid_cohorts.add(sched[room][time][-1])

    return set(cohorts).difference(invalid_cohorts)

def add_lectures_to_db():
    '''
    Add the lecture objects to the database so the UI can read & display them
    '''
    db = r".\database\database.db"  # database.db file path
    connection = create_connection(db)
    for lec in lecture_objs:
        addLectureItem(connection, lec)
    close_connection(connection)
    return

# testing only
def is_valid_sched(lectures, sched):

    pcom_lec_IDs = {
        'pcom A': [c.ID for c in lectures['pcomA']],
        'pcom B': [c.ID for c in lectures['pcomB']],
    }

    bcom_lec_IDs = {
        'bcom A': [c.ID for c in lectures['bcomA']],
        'bcom B': [c.ID for c in lectures['bcomB']],
    }

    transposed = sched.T
    for time in transposed.columns.tolist():
        pcom_A = [c[-1] for c in transposed[time].tolist() if
                  c[:-2] in pcom_lec_IDs['pcom A']]
        pcom_B = [c[-1] for c in transposed[time].tolist() if
                  c[:-2] in pcom_lec_IDs['pcom B']]
        bcom_A = [c[-1] for c in transposed[time].tolist() if
                  c[:-2] in bcom_lec_IDs['bcom A']]
        bcom_B = [c[-1] for c in transposed[time].tolist() if
                  c[:-2] in bcom_lec_IDs['bcom B']]

        if len(pcom_A) != len(set(pcom_A)) or len(pcom_B) != len(set(pcom_B)) or \
           len(bcom_A) != len(set(bcom_A)) or len(bcom_B) != len(set(bcom_B)):

            # print(f"\n\nconflict at {time}\n")
            # print(sched)
            return True
    return False
#===============================================================================


#============================= LECTURE SCHEDULING ==============================
def make_core_lecture_sched(lectures: Dict[str, List[Course]], 
                            cohorts: Dict[str, List[str]],
                            c_hours: Dict[str, int], 
                            sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes a dict of pcom & bcom lectures for terms A & B, a dict of course_hours, 
    and a room list to create a schedule for a single day and return it as a 
    DataFrame. Courses are scheduled by pcom/bcom and term, moving from rooms
    left to right, starting at 8 am.
    '''

    # lists of course IDs used to ensure no scheduling conflicts occur
    pcomA_strs = [c.ID for c in lectures['pcomA']]
    pcomB_strs = [c.ID for c in lectures['pcomB']]
    bcomA_strs = [c.ID for c in lectures['bcomA']]
    bcomB_strs = [c.ID for c in lectures['bcomB']]

    # parse cohorts for each program/term
    pcomA_cohorts = cohorts['pcomA']
    pcomB_cohorts = cohorts['pcomB']
    bcomA_cohorts = cohorts['bcomA']
    bcomB_cohorts = cohorts['bcomB']

    # filter out courses that dont need to be scheduled
    pcomA = filter_courses(lectures['pcomA'], sched, c_hours)
    pcomB = filter_courses(lectures['pcomB'], sched, c_hours)
    bcomA = filter_courses(lectures['bcomA'], sched, c_hours)
    bcomB = filter_courses(lectures['bcomB'], sched, c_hours)
    
    # schedule as many courses as possible
    most_courses = max(
        pcomA, pcomB, bcomA, bcomB, key=lambda x: len(x)
    )

    for i in range(len(most_courses)):

        if len(pcomB) > i:
            sched = add_lec(pcomB[i], pcomB_cohorts, c_hours, pcomB_strs, sched)

        if len(bcomB) > i:
            sched = add_lec(bcomB[i], bcomB_cohorts, c_hours, bcomB_strs, sched)
            
        if len(bcomA) > i:
            sched = add_lec(bcomA[i], bcomA_cohorts, c_hours, bcomA_strs, sched)
            
        if len(pcomA) > i:
            sched = add_lec(pcomA[i], pcomA_cohorts, c_hours, pcomA_strs, sched)

    return sched

def make_program_lecture_sched(lectures: Dict[str, List[Course]], 
                               cohorts: Dict[str, List[str]],
                               c_hours: Dict[str, int], 
                               sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes a dict of program lectures for terms A & B, a dict of course_hours, 
    and a room list to create a schedule for a single day and return it as a 
    DataFrame. Courses are scheduled by program and term, moving from rooms
    left to right, starting at 8 am.
    '''

    # lists of course IDs used to ensure no scheduling conflicts occur
    pmA_strs  = [c.ID for c in lectures['pmA']]
    pmB_strs  = [c.ID for c in lectures['pmB']]
    baA_strs  = [c.ID for c in lectures['baA']]
    baB_strs  = [c.ID for c in lectures['baB']]
    glmA_strs = [c.ID for c in lectures['glmA']]
    glmB_strs = [c.ID for c in lectures['glmB']]
    dxdA_strs = [c.ID for c in lectures['dxdA']]
    dxdB_strs = [c.ID for c in lectures['dxdB']]
    bkA_strs  = [c.ID for c in lectures['bkA']]
    bkB_strs  = [c.ID for c in lectures['bkB']]

    # parse cohorts for each program/term
    pmA_cohorts  = cohorts['pmA']
    pmB_cohorts  = cohorts['pmB']
    baA_cohorts  = cohorts['baA']
    baB_cohorts  = cohorts['baB']
    glmA_cohorts = cohorts['glmA']
    glmB_cohorts = cohorts['glmB']
    dxdA_cohorts = cohorts['dxdA']
    dxdB_cohorts = cohorts['dxdB']
    bkA_cohorts  = cohorts['bkA']
    bkB_cohorts  = cohorts['bkB']

    # filter out courses that dont need scheduling
    pmA  = filter_courses(lectures['pmA'],  sched, c_hours)
    pmB  = filter_courses(lectures['pmB'],  sched, c_hours)
    baA  = filter_courses(lectures['baA'],  sched, c_hours)
    baB  = filter_courses(lectures['baB'],  sched, c_hours)
    glmA = filter_courses(lectures['glmA'], sched, c_hours)
    glmB = filter_courses(lectures['glmB'], sched, c_hours)
    dxdA = filter_courses(lectures['dxdA'], sched, c_hours)
    dxdB = filter_courses(lectures['dxdB'], sched, c_hours)
    bkA  = filter_courses(lectures['bkA'],  sched, c_hours)
    bkB  = filter_courses(lectures['bkB'],  sched, c_hours)
    
    # schedule as many courses as possible
    most_courses = max(
        pmA, pmB, baA, baB, glmA, glmB, dxdA, dxdB, bkA, bkB, 
        key=lambda x: len(x)
    )
    for i in range(len(most_courses)):

        if len(pmA) > i:
            sched = add_lec(pmA[i], pmA_cohorts, c_hours, pmA_strs, sched)

        if len(pmB) > i:
            sched = add_lec(pmB[i], pmB_cohorts, c_hours, pmB_strs, sched)

        if len(baA) > i:
            sched = add_lec(baA[i], baA_cohorts, c_hours, baA_strs, sched)

        if len(baB) > i:
            sched = add_lec(baB[i], baB_cohorts, c_hours, baB_strs, sched)
            
        if len(glmA) > i:
            sched = add_lec(glmA[i], glmA_cohorts, c_hours, glmA_strs, sched)

        if len(glmB) > i:
            sched = add_lec(glmB[i], glmB_cohorts, c_hours, glmB_strs, sched)

        if len(dxdA) > i:
            sched = add_lec(dxdA[i], dxdA_cohorts, c_hours, dxdA_strs, sched)

        if len(dxdB) > i:
            sched = add_lec(dxdB[i], dxdB_cohorts, c_hours, dxdB_strs, sched)
            
        if len(bkA) > i:
            sched = add_lec(bkA[i], bkA_cohorts, c_hours, bkA_strs, sched)

        if len(bkB) > i:
            sched = add_lec(bkB[i], bkB_cohorts, c_hours, bkB_strs, sched)

    return sched

def add_lec(course: Course, cohorts: List[str], course_hours: Dict[str, int],
            invalid_courses: List[str], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Checks when/if a given course can be scheduled and if so, what order the 
    cohorts should be scheduled. Returns an updated schedule if the course can
    be added, otherwise this returns an unaltered schedule
    '''

    if course.isOnline or course.hasLab:
        return sched

    blocks = get_time_slot_count(course, course_hours)
    
    #print(f"blocks: {blocks}")

    # dict mapping room names to available start times (indexes, not strs)
    open_times = get_available_times(sched, blocks, len(cohorts))
    #print(f"open times: {open_times}, cohort count: {len(cohorts)}")
    if (open_times == {}):
        return sched

    cohort_times = {}
    for room, times in open_times.items():
        # for each start time, find out which cohorts can be scheduled 
        for start in times:
            end = start + blocks
            valid = get_valid_cohorts(
                invalid_courses, start, end, cohorts, room, sched
            )
            # only add cohorts we havent seen yet
            for cohort_ID in valid.difference(set(cohort_times.keys())):
                # only add rooms & start times that have not been assigned yet
                if (room, start) not in cohort_times.values():
                    cohort_times[cohort_ID] = (room, start)
                

    # not all cohorts can fit in the schedule
    if len(cohort_times.keys()) < len(cohorts):
        return sched

    for ID, time_slot in cohort_times.items():

        room, start = time_slot
        room_index  = sched.columns.get_loc(room)
        start_label = list(sched.index)[start]

        # store the scheduled course's info in a lecture object
        lecture_objs.append(
            Lecture(
                course.ID, course.title, course.termHours, course.term,
                course.duration, course.isCore, course.isOnline, course.hasLab,
                course.preReqs, ID, room, week, day, start_label
            )
        )

        course_strs = [course.ID + '-' + ID] * blocks
        sched.iloc[start:(start+blocks), room_index] = course_strs

    return sched
#===============================================================================
    
    
#=============================== LAB SCHEDULING ================================
def make_core_lab_sched(lectures: Dict[str, List[Course]], 
                        labs: Dict[str, List[Course]],
                        cohorts: Dict[str, List[str]], 
                        c_hours: Dict[str, int], 
                        lec_sched: pd.DataFrame, 
                        lab_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the existing lecture schedule and information on what labs to schedule,
    and tries to schedule each lab without any conflicts with already scheduled
    courses
    '''
    # lists of lecture & lab IDs used to ensure no scheduling conflicts occur
    pcomA_strs = [c.ID for c in lectures['pcomA']]+[c.ID for c in labs['pcomA']] 
    pcomB_strs = [c.ID for c in lectures['pcomB']]+[c.ID for c in labs['pcomB']]
    bcomA_strs = [c.ID for c in lectures['bcomA']]+[c.ID for c in labs['bcomA']]
    bcomB_strs = [c.ID for c in lectures['bcomB']]+[c.ID for c in labs['bcomB']]
    
    # parse cohorts for each program/term
    pcomA_cohorts = cohorts['pcomA']
    pcomB_cohorts = cohorts['pcomB']
    bcomA_cohorts = cohorts['bcomA']
    bcomB_cohorts = cohorts['bcomB']
    
    # filter out labs that dont need scheduling
    pcomA = filter_courses(labs['pcomA'], lab_sched, c_hours)
    pcomB = filter_courses(labs['pcomB'], lab_sched, c_hours)
    bcomA = filter_courses(labs['bcomA'], lab_sched, c_hours)
    bcomB = filter_courses(labs['bcomB'], lab_sched, c_hours)
    
    # schedule as many labs as possible
    most_courses = max(
        pcomA, pcomB, bcomA, bcomB, key=lambda x: len(x)
    )
    for i in range(len(most_courses)):
        
        if len(pcomA) > i:
            lab_sched = add_lab(
                pcomA[i], pcomA_cohorts, c_hours, pcomA_strs, lec_sched, lab_sched
            )  
        if len(pcomB) > i:
            lab_sched = add_lab(
                pcomB[i], pcomB_cohorts, c_hours, pcomB_strs, lec_sched, lab_sched
            )
        if len(bcomA) > i:
            lab_sched = add_lab(
                bcomA[i], bcomA_cohorts, c_hours, bcomA_strs, lec_sched, lab_sched
            )
        if len(bcomB) > i:
            lab_sched = add_lab(
                bcomB[i], bcomB_cohorts, c_hours, bcomB_strs, lec_sched, lab_sched
            )
                
    return lab_sched
   

def make_program_lab_sched(lectures: Dict[str, List[Course]],
                           labs: Dict[str, List[Course]],
                           cohorts: Dict[str, List[str]],
                           c_hours: Dict[str, int],
                           lec_sched: pd.DataFrame,
                           lab_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the existing lecture schedule and information on what labs to schedule,
    and tries to schedule each lab at a time when it won't conflict with lectures
    '''
    # lists of lecture & lab IDs used to ensure no scheduling conflicts occur
    pmA_strs  = [c.ID for c in lectures['pmA']]  + [c.ID for c in labs['pmA']]
    pmB_strs  = [c.ID for c in lectures['pmB']]  + [c.ID for c in labs['pmB']]
    baA_strs  = [c.ID for c in lectures['baA']]  + [c.ID for c in labs['baA']]
    baB_strs  = [c.ID for c in lectures['baB']]  + [c.ID for c in labs['baB']]
    glmA_strs = [c.ID for c in lectures['glmA']] + [c.ID for c in labs['glmA']]
    glmB_strs = [c.ID for c in lectures['glmB']] + [c.ID for c in labs['glmB']]
    dxdA_strs = [c.ID for c in lectures['dxdA']] + [c.ID for c in labs['dxdA']]
    dxdB_strs = [c.ID for c in lectures['dxdB']] + [c.ID for c in labs['dxdB']]
    bkA_strs  = [c.ID for c in lectures['bkA']]  + [c.ID for c in labs['bkA']]
    bkB_strs  = [c.ID for c in lectures['bkB']]  + [c.ID for c in labs['bkB']]

    # parse cohorts for each program/term
    pmA_cohorts  = cohorts['pmA']
    pmB_cohorts  = cohorts['pmB']
    baA_cohorts  = cohorts['baA']
    baB_cohorts  = cohorts['baB']
    glmA_cohorts = cohorts['glmA']
    glmB_cohorts = cohorts['glmB']
    dxdA_cohorts = cohorts['dxdA']
    dxdB_cohorts = cohorts['dxdB']
    bkA_cohorts  = cohorts['bkA']
    bkB_cohorts  = cohorts['bkB']

    # filter out courses that dont need scheduling
    pmA  = filter_courses(labs['pmA'],  lab_sched, c_hours)
    pmB  = filter_courses(labs['pmB'],  lab_sched, c_hours)
    baA  = filter_courses(labs['baA'],  lab_sched, c_hours)
    baB  = filter_courses(labs['baB'],  lab_sched, c_hours)
    glmA = filter_courses(labs['glmA'], lab_sched, c_hours)
    glmB = filter_courses(labs['glmB'], lab_sched, c_hours)
    dxdA = filter_courses(labs['dxdA'], lab_sched, c_hours)
    dxdB = filter_courses(labs['dxdB'], lab_sched, c_hours)
    bkA  = filter_courses(labs['bkA'],  lab_sched, c_hours)
    bkB  = filter_courses(labs['bkB'],  lab_sched, c_hours)

    # schedule as many courses as possible
    most_courses = max(
        pmA, pmB, baA, baB, glmA, glmB, dxdA, dxdB, bkA, bkB,
        key=lambda x: len(x)
    )
    for i in range(len(most_courses)):

        if len(pmA) > i:
            lab_sched = add_lab(
                pmA[i], pmA_cohorts, c_hours, pmA_strs, lec_sched, lab_sched
            )
        if len(pmB) > i:
            lab_sched = add_lab(
                pmB[i], pmB_cohorts, c_hours, pmB_strs, lec_sched, lab_sched
            )
        if len(baA) > i:
            lab_sched = add_lab(
                baA[i], baA_cohorts, c_hours, baA_strs, lec_sched, lab_sched
            )
        if len(baB) > i:
            lab_sched = add_lab(
                baB[i], baB_cohorts, c_hours, baB_strs, lec_sched, lab_sched
            )
        if len(glmA) > i:
            lab_sched = add_lab(
                glmA[i], glmA_cohorts, c_hours, glmA_strs, lec_sched, lab_sched
            )
        if len(glmB) > i:
            lab_sched = add_lab(
                glmB[i], glmB_cohorts, c_hours, glmB_strs, lec_sched, lab_sched
            )
        if len(dxdA) > i:
            lab_sched = add_lab(
                dxdA[i], dxdA_cohorts, c_hours, dxdA_strs, lec_sched, lab_sched
            )
        if len(dxdB) > i:
            lab_sched = add_lab(
                dxdB[i], dxdB_cohorts, c_hours, dxdB_strs, lec_sched, lab_sched
            )
        if len(bkA) > i:
            lab_sched = add_lab(
                bkA[i], bkA_cohorts, c_hours, bkA_strs, lec_sched, lab_sched
            )
        if len(bkB) > i:
            lab_sched = add_lab(
                bkB[i], bkB_cohorts, c_hours, bkB_strs, lec_sched, lab_sched
            )

    return lab_sched
         

def add_lab(lab: Course, cohorts: List[str], 
            course_hours: Dict[str, int], invalid_courses: List[str], 
            lec_sched: pd.DataFrame, lab_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Checks when/if a given lab can be scheduled without conflicting with any 
    lectures, what order the lab cohorts should be scheduled. Returns an updated 
    schedule if the lab can be added, otherwise this returns an unaltered schedule
    '''
    blocks = get_time_slot_count(lab, course_hours)

    # dict mapping room names to available start times (indexes, not strs)
    open_times = get_available_times(lab_sched, blocks, len(cohorts))
    
    if (open_times == {}):
        return lab_sched

    cohort_times = {}
    for room, times in open_times.items():
        # for each start time, find out which cohorts can be scheduled
        for start in times:
            end = start + blocks
            valid = get_valid_cohorts(
                invalid_courses, start, end, cohorts, room, lec_sched.join(lab_sched)
            )
            # only add cohorts we havent seen yet
            for cohort_ID in valid.difference(set(cohort_times.keys())):
                # only add rooms & start times that have not been assigned yet
                if (room, start) not in cohort_times.values():
                    cohort_times[cohort_ID] = (room, start)
        
    for ID, time_slot in cohort_times.items():

        room, start = time_slot
        room_index = lab_sched.columns.get_loc(room)
        start_label = list(lab_sched.index)[start]

        # store the scheduled course's info in a lecture object
        lecture_objs.append(
            Lecture(
                lab.ID, lab.title, lab.termHours, lab.term,
                lab.duration, lab.isCore, lab.isOnline, lab.hasLab,
                lab.preReqs, ID, room, week, day, start_label
            )
        )

        course_strs = [lab.ID + '-' + ID] * blocks
        lab_sched.iloc[start:(start+blocks), room_index] = course_strs

    return lab_sched

#============================== ONLINE SCHEDULING ==============================
def make_core_online_sched(lectures: Dict[str, List[Course]],
                      labs: Dict[str, List[Course]],
                      online: Dict[str, List[Course]], 
                      course_hours: Dict[str, int], 
                      curr_sched: pd.DataFrame, 
                      onl_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the existing lecture schedule and information on what online courses
    to schedule, and checks at each row (time) if an online course can be 
    scheduled without any conflicts. Courses also cant be within 1.5 hours 
    of in-person courses in the same program/term
    '''
    
    # lists of course IDs used to ensure no scheduling conflicts occur
    pcomA_strs = [c.ID for c in lectures['pcomA']]+[c.ID for c in labs['pcomA']] 
    pcomB_strs = [c.ID for c in lectures['pcomB']]+[c.ID for c in labs['pcomB']]
    bcomA_strs = [c.ID for c in lectures['bcomA']]+[c.ID for c in labs['bcomA']]
    bcomB_strs = [c.ID for c in lectures['bcomB']]+[c.ID for c in labs['bcomB']]

    # filter out courses that dont need scheduling
    pcomA = filter_courses(online['pcomA'], onl_sched, course_hours)
    pcomB = filter_courses(online['pcomB'], onl_sched, course_hours)
    bcomA = filter_courses(online['bcomA'], onl_sched, course_hours)
    bcomB = filter_courses(online['bcomB'], onl_sched, course_hours)
    
    # avdm 0260 should be scheduled at the end of the term
    # if (day < 23):
    #     valid_bcomB = [o for o in valid_bcomB if o.ID != "AVDM 0260"]
    
    # schedule as many courses as possible
    most_courses = max(
        pcomA, pcomB, bcomA, bcomB, key=lambda x: len(x)
    )
    for i in range(len(most_courses)):

        if len(pcomA) > i:
            onl_sched = add_onl(
                pcomA[i], course_hours, pcomA_strs, curr_sched, onl_sched
            )
        if len(pcomB) > i:
            onl_sched = add_onl(
                pcomB[i], course_hours, pcomB_strs, curr_sched, onl_sched
            )
        if len(bcomA) > i:
            onl_sched = add_onl(
                bcomA[i], course_hours, bcomA_strs, curr_sched, onl_sched
            )
        if len(bcomB) > i:
            onl_sched = add_onl(
                bcomB[i], course_hours, bcomB_strs, curr_sched, onl_sched
            )
            
    return onl_sched


def make_program_online_sched(lectures: Dict[str, List[Course]],
                              labs: Dict[str, List[Course]],
                              online: Dict[str, List[Course]],
                              c_hours: Dict[str, int],
                              curr_sched: pd.DataFrame,
                              onl_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the existing lecture schedule and information on what online courses
    to schedule, and checks at each row (time) if an online course can be 
    scheduled without any conflicts. Courses also cant be within 1.5 hours 
    of in-person courses in the same program/term
    '''
    # lists of lecture & lab IDs used to ensure no scheduling conflicts occur
    pmA_strs  = [c.ID for c in lectures['pmA']]  + [c.ID for c in labs['pmA']]
    pmB_strs  = [c.ID for c in lectures['pmB']]  + [c.ID for c in labs['pmB']]
    baA_strs  = [c.ID for c in lectures['baA']]  + [c.ID for c in labs['baA']]
    baB_strs  = [c.ID for c in lectures['baB']]  + [c.ID for c in labs['baB']]
    glmA_strs = [c.ID for c in lectures['glmA']] + [c.ID for c in labs['glmA']]
    glmB_strs = [c.ID for c in lectures['glmB']] + [c.ID for c in labs['glmB']]
    dxdA_strs = [c.ID for c in lectures['dxdA']] + [c.ID for c in labs['dxdA']]
    dxdB_strs = [c.ID for c in lectures['dxdB']] + [c.ID for c in labs['dxdB']]
    bkA_strs  = [c.ID for c in lectures['bkA']]  + [c.ID for c in labs['bkA']]
    bkB_strs  = [c.ID for c in lectures['bkB']]  + [c.ID for c in labs['bkB']]

    # filter out courses that dont need scheduling
    pmA  = filter_courses(online['pmA'],  onl_sched, c_hours)
    pmB  = filter_courses(online['pmB'],  onl_sched, c_hours)
    baA  = filter_courses(online['baA'],  onl_sched, c_hours)
    baB  = filter_courses(online['baB'],  onl_sched, c_hours)
    glmA = filter_courses(online['glmA'], onl_sched, c_hours)
    glmB = filter_courses(online['glmB'], onl_sched, c_hours)
    dxdA = filter_courses(online['dxdA'], onl_sched, c_hours)
    dxdB = filter_courses(online['dxdB'], onl_sched, c_hours)
    bkA  = filter_courses(online['bkA'],  onl_sched, c_hours)
    bkB  = filter_courses(online['bkB'],  onl_sched, c_hours)

    # schedule as many courses as possible
    most_courses = max(
        pmA, pmB, baA, baB, glmA, glmB, dxdA, dxdB, bkA, bkB,
        key=lambda x: len(x)
    )
    for i in range(len(most_courses)):

        if len(pmA) > i:
            onl_sched = add_onl(
                pmA[i], c_hours, pmA_strs, curr_sched, onl_sched
            )
        if len(pmB) > i:
            onl_sched = add_onl(
                pmB[i], c_hours, pmB_strs, curr_sched, onl_sched
            )
        if len(baA) > i:
            onl_sched = add_onl(
                baA[i], c_hours, baA_strs, curr_sched, onl_sched
            )
        if len(baB) > i:
            onl_sched = add_onl(
                baB[i], c_hours, baB_strs, curr_sched, onl_sched
            )
        if len(glmA) > i:
            onl_sched = add_onl(
                glmA[i], c_hours, glmA_strs, curr_sched, onl_sched
            )
        if len(glmB) > i:
            onl_sched = add_onl(
                glmB[i], c_hours, glmB_strs, curr_sched, onl_sched
            )
        if len(dxdA) > i:
            onl_sched = add_onl(
                dxdA[i], c_hours, dxdA_strs, curr_sched, onl_sched
            )
        if len(dxdB) > i:
            onl_sched = add_onl(
                dxdB[i], c_hours, dxdB_strs, curr_sched, onl_sched
            )
        if len(bkA) > i:
            onl_sched = add_onl(
                bkA[i], c_hours, bkA_strs, curr_sched, onl_sched
            )
        if len(bkB) > i:
            onl_sched = add_onl(
                bkB[i], c_hours, bkB_strs, curr_sched, onl_sched
            )

    return onl_sched


def add_onl(online: Course, course_hours: Dict[str, int], invalid_courses: List[str],
            curr_sched: pd.DataFrame, onl_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Checks the current schedule to see if an online course can be 
    scheduled without any conflicts. Courses cannot be within 1.5 hours of an
    in-person class in the same program/term. Cohorts are not required since 
    online courses are not restricted by classroom capacity
    '''

    blocks = get_time_slot_count(online, course_hours)

    # dict mapping room names to available start times (indexes, not strs)
    open_times = get_available_times(onl_sched, blocks, 1)
    
    if (open_times == {}):
        return onl_sched
    
    # check if each timeslot is not within 1.5 hours of a lecture 
    for times in open_times.values():
        for start in times:
            end = start + blocks
            
            if not online_course_overlap(curr_sched, invalid_courses, start, end):
                
                new_lec = Lecture(
                    online.ID, online.title, online.termHours, 
                    online.term, online.duration, online.isCore,
                    online.isOnline, online.hasLab, online.preReqs, "", 
                    list(onl_sched.columns)[0], week, day, start
                )
                lecture_objs.append(new_lec)
                
                onl_sched.iloc[start:end, 0] = ([online.ID] * blocks)
                break
    
    return onl_sched

def online_course_overlap(curr_sched: pd.DataFrame, invalid_courses: List[str], 
                          start: int, end: int) -> bool:
    '''
    Compares a possible start & end time for an online course and returns a 
    boolean indicating if the course can be scheduled at that time.
    '''
    for room in curr_sched.columns:
        for idx in range(max(start-3, 0), end+2):
            if (curr_sched.iloc[idx][room])[:-2] in invalid_courses:
                return False
    return True
#===============================================================================

def create_core_term_schedule(lectures: Dict[str, List[Course]], 
                              labs: Dict[str, List[Course]],
                              online: Dict[str, List[Course]], 
                              cohorts: Dict[str, List[str]], 
                              rooms: List[Classroom],
                              start_day: datetime.date, 
                              holidays: List[datetime.date]) -> Dict[str, pd.DataFrame]:
    '''
    Main schedule creation function that makes 26 single-day schedules (mon/wed, 13 weeks)
    each as a pandas DataFrame, and returns them in a dictionary
    '''

    global day, week, lecture_objs
    
    day = start_day
    end_day = start_day + datetime.timedelta(weeks=13)
    
    all_courses = list(
        chain(*list(lectures.values())+list(labs.values())+list(online.values()))
    )

    course_hours = get_course_hours(all_courses)

    # create schedules for the first day, then reference this when making 
    # subsequent schedules to get consistent times and rooms for courses
    prev_lecs = create_empty_schedule([room for room in rooms if not room.isLab 
                                       and not room.ID.startswith('ONLINE')])
    prev_labs = create_empty_schedule([room for room in rooms if room.isLab])
    prev_onls = create_empty_schedule([room for room in rooms if room.ID == 'ONLINE'])
    
    full_schedule = {}
    invalid = 0

    while day < end_day:
        
        if day in holidays:
            full_schedule[day] = (f"HOLIDAY")
            if (day.weekday() == 0):
                day += datetime.timedelta(days=2)
            elif (day.weekday() == 2):
                day += datetime.timedelta(days=5)
            continue
        
        lecture_sched = make_core_lecture_sched(
            lectures, cohorts,
            course_hours, prev_lecs
        )
        
        if is_valid_sched(lectures, lecture_sched): 
            invalid += 1
            
        lab_sched = make_core_lab_sched(
            lectures, labs, cohorts, course_hours, lecture_sched, prev_labs
        )
        
        joined_sched = lecture_sched.join((lab_sched))
        
        online_sched = make_core_online_sched(
            lectures, labs, online, course_hours, joined_sched, prev_onls
        )
        
        full_day_sched = joined_sched.join(online_sched)
        full_schedule[day] = (full_day_sched)
        course_hours = update_course_hours(course_hours, full_day_sched)
        
        prev_lecs = update_schedule(course_hours, lecture_sched)
        prev_labs = update_schedule(course_hours, lab_sched)
        prev_onls = update_schedule(course_hours, online_sched)
        
        
        if (day.weekday() == 0):
            day += datetime.timedelta(days=2)
        elif (day.weekday() == 2):
            day += datetime.timedelta(days=5)

        
    print(f"\n\nINVALID COUNT: {invalid}\n\n")
    pprint(course_hours)
        
    add_lectures_to_db()
    return full_schedule

def create_program_term_schedule(lectures: Dict[str, List[Course]],
                                 labs: Dict[str, List[Course]],
                                 online: Dict[str, List[Course]],
                                 cohorts: Dict[str, List[str]],
                                 rooms: List[Classroom],
                                 start_day: datetime.date, 
                                 holidays: List[datetime.date]) -> Dict[str, pd.DataFrame]:
    '''
    Main schedule creation function that makes 26 single-day schedules (tue/thu, 13 weeks)
    each as a pandas DataFrame, and returns them in a dictionary
    '''

    global day, week, lecture_objs

    day = start_day
    end_day = start_day + datetime.timedelta(weeks=13)

    all_courses = list(
        chain(*list(lectures.values())+list(labs.values())+list(online.values()))
    )

    course_hours = get_course_hours(all_courses)

    # create schedules for the first day, then reference this when making
    # subsequent schedules to get consistent times and rooms for courses
    prev_lecs = create_empty_schedule([r for r in rooms if not r.isLab
                                       and not r.ID.startswith('ONLINE')])
    prev_labs = create_empty_schedule([r for r in rooms if r.isLab])
    prev_onls = create_empty_schedule([r for r in rooms if r.ID == 'ONLINE'])

    full_schedule = {}
    
    while day < end_day:

        if day in holidays:
            full_schedule[day] = (f"HOLIDAY")
            if (day.weekday() == 0):
                day += datetime.timedelta(days=2)
            elif (day.weekday() == 2):
                day += datetime.timedelta(days=5)
            continue

        lecture_sched = make_program_lecture_sched(
            lectures, cohorts,
            course_hours, prev_lecs
        )

        lab_sched = make_program_lab_sched(
            lectures, labs, cohorts, course_hours, lecture_sched, prev_labs
        )

        joined_sched = lecture_sched.join((lab_sched))

        online_sched = make_program_online_sched(
            lectures, labs, online, course_hours, joined_sched, prev_onls
        )
        
        full_day_sched = joined_sched.join(online_sched)
        full_schedule[day] = (full_day_sched)
        course_hours = update_course_hours(course_hours, full_day_sched)

        prev_lecs = update_schedule(course_hours, lecture_sched)
        prev_labs = update_schedule(course_hours, lab_sched)
        prev_onls = update_schedule(course_hours, online_sched)

        if (day.weekday() == 0):
            day += datetime.timedelta(days=2)
        elif (day.weekday() == 2):
            day += datetime.timedelta(days=5)

    pprint(course_hours)

    add_lectures_to_db()
    return full_schedule



def getHolidaysMonWed(fallYear):
    '''
    Pass the year of the fall term, and will make a list of holidays that land on 
    mondays and wednesdays in the 3 terms. Returns list of datetime objects
    '''
    holidayList = []
    nextYear = fallYear + 1
    FallmonthList = [9,10,11]
    TARD = datetime.date(fallYear,9,30)
    nextMonthList = [1,2,3,4, 5,6,7,8]
    
    #FALL:
    for ptr in holidays.Canada(years = fallYear).items():
        if ( ptr[0].month in FallmonthList):
            if("Observed" not in ptr[1] and (ptr[0].weekday() == 0 or ptr[0].weekday() == 2)):
                holidayList.append(ptr[0])
    if(TARD.weekday()== 0 or TARD.weekday() == 2):
        holidayList.insert(1,TARD)
    #WIN/SPRING OF NEXT YEAR
    for ptr in holidays.Canada(years = nextYear).items():
        if ( ptr[0].month in nextMonthList and (ptr[0].weekday() == 0 or ptr[0].weekday() == 2)):
            if("Observed" not in ptr[1] and 'New Year' not in ptr[1]):
                holidayList.append(ptr[0])
    return holidayList  

def getHolidaysTuesThurs(fallYear):
    '''
    Pass the year of the fall term, and will make a list of holidays that land on 
    Tuesdays and Thursdays in the 3 terms. Returns list of datetime objects
    '''
    holidayList = []
    nextYear = fallYear + 1
    FallmonthList = [9,10,11]
    TARD = datetime.date(fallYear,9,30)
    nextMonthList = [1,2,3,4, 5,6,7,8]

    #FALL:
    for ptr in holidays.Canada(years = fallYear).items():
        if ( ptr[0].month in FallmonthList):
            if("Observed" not in ptr[1] and (ptr[0].weekday() == 1 or ptr[0].weekday() == 3)):
                holidayList.append(ptr[0])
    if(TARD.weekday()== 1 or TARD.weekday() == 3):
        holidayList.insert(1,TARD)

    #WIN/SPRING OF NEXT YEAR
    for ptr in holidays.Canada(years = nextYear).items():
        if ( ptr[0].month in nextMonthList and (ptr[0].weekday() == 1 or ptr[0].weekday() == 3)):
            if("Observed" not in ptr[1] and 'New Year' not in ptr[1]):
                holidayList.append(ptr[0])  
    return holidayList  


'''reading week in fall - happens after week with remb.day or week after if it lands on a weekend'''
'''reading week in wint - happens after week with fam day in feb or week after if it lands on a weekend '''
'''No reading break in sp/su'''

def getFallStartDay(year):
    '''Returns datetime object of the first day of fall term in passed year
    first Wednesday of September '''
    sept1 = datetime.date(year,9,1)
    offset = 2-sept1.weekday() #weekday = 2 means wednesday
    if offset < 0:
        offset+=7
    return sept1+datetime.timedelta(offset)

def getWinterStartDay(year):
    '''Returns datetime object of the first day of winter term in passed year
    first Wednesday of Janurary'''
    jan1 = datetime.date(year,1,1)
    offset = 2-jan1.weekday() #weekday = 2 means wednesday
    if offset < 0:
        offset+=7
    return jan1+datetime.timedelta(offset)
def getSpringStartDay(year):
    '''Returns datetime object of the first day of spring term in passed year
    May 1st if lands on a weekday, otherwise the first Monday of May'''
    startday = datetime.date(year,5,1) #may 1
    if (startday.weekday() == 5):
        startday = datetime.date(year,5,3)
    if(startday.weekday() == 6):
        startday = datetime.date(year,5,2)
    return startday

