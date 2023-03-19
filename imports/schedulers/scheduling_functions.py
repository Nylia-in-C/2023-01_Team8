import os, sys
import math
import datetime
import pandas as pd
import numpy as np
import static_frame as sf
from imports.classes.courses import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
import string
from typing import *
from itertools import chain

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

#===================== TODOs (in no particular order) ==========================

#TODO: Schedule pcom_0130 & pcom_0140 halfway through term
#       - create global var 'day', when creating day sched:
#           if day == 13, move these courses to the front of the list of courses being scheduled

#TODO: add a buffer before/after online classes (cant be immediately before/after in-person courses)
#       - schedule them at the same time as in-person courses 
#           (use a '-' to mark the buffer, so no in-person courses are scheduled at that time)
#           

#TODO: get actual cohort count from fillClassrooms.py, make sure this stuff works for any number of cohorts


#TODO: check for holidays (might be easier if we use date objects rather than day 1, day 2, etc.) 

#TODO: create lecture objects either:
#           - after the schedule is made, or
#           - before: store each lecture's ID in the dataframe & update it's hours when it gets added to the schedule


# assuming ~100-120 new students/term requires 4 different lecture groups for each course
COHORT_COUNT = 6
# ==============================================================================

def create_empty_schedule(room_list: List[Classroom]) -> pd.DataFrame:
    '''
    This function creates an empty pandas dataframe to represent the schedule 
    for a single day. The column headers are room numbers and the row indexes 
    are times (half hour increments)
    '''

    # 8 AM - 5 PM in half-hour increments
    times = [datetime.time(i, j).strftime("%H:%M")
             for i in range(8, 17) for j in [0, 30]]
    times.append(datetime.time(17, 0).strftime("%H:%M"))

    sched = pd.DataFrame(index=times)
    
    for room in room_list:
        sched[room.ID] = [""] * 19

    return sched


def get_course_hours(courses: List[Course]) -> Dict[str, int]:
    '''
    Create 2 dictionaries that will be used to keep track of how many hours
    a given course has, and how many hours it has left. One dictionary handles
    lecture hours, the other handles lab hours 
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
    Uses the previous day's schedule to update the remaining lecture hours for each course
    '''
    # dont update the same course twice
    seen = set()

    # get number of hours for each course on the schedule
    for room in prev_schedule.columns:
        courses = prev_schedule[room].tolist()
        for course in courses:
            if (course == ""):
                continue

            # remove cohort identifier
            course_name = course[:-2]

            if course_name in seen:
                continue

            seen.add(course_name)

            scheduled_hours = (courses.count(course)) * 0.5
            course_hours[course_name]['scheduled'] += scheduled_hours
            course_hours[course_name]['remaining'] -= scheduled_hours

    return course_hours

def make_lecture_schedule(term_A_pcom: List[Course], term_B_pcom: List[Course], 
                          term_A_bcom: List[Course], term_B_bcom: List[Course],
                          course_hours: Dict[str, int], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes lists of pcom & bcom lectures for terms A & B, a dictionary of course_hours, 
    and a room list to create a schedule for a single day and return it as a 
    DataFrame. Courses are scheduled by pcom/bcom and term, moving from rooms
    left to right, starting at 8 am, where each cohort takes up half a day.
    '''

    # dont schedule courses that are already in the previous day's schedule,
    # or ones that have already been fully scheduled
    already_scheduled = [course[:-2] for course in sched.values.flatten()]
    
    term_A_pcom = [course for course in term_A_pcom if
                   course.ID not in already_scheduled and
                   course_hours[course.ID]['remaining'] > 0]
    term_B_pcom = [course for course in term_B_pcom if
                   course.ID not in already_scheduled and
                   course_hours[course.ID]['remaining'] > 0]
    term_A_bcom = [course for course in term_A_bcom if
                   course.ID not in already_scheduled and
                   course_hours[course.ID]['remaining'] > 0]
    term_B_bcom = [course for course in term_B_bcom if
                   course.ID not in already_scheduled and
                   course_hours[course.ID]['remaining'] > 0]
    
    # sort courses by required hours in descending order
    term_A_pcom.sort(key=lambda x: x.termHours, reverse=True)
    term_B_pcom.sort(key=lambda x: x.termHours, reverse=True)
    term_A_bcom.sort(key=lambda x: x.termHours, reverse=True)
    term_B_bcom.sort(key=lambda x: x.termHours, reverse=True)

        
    if (len(term_A_pcom) > 0):
        sched = add_courses(term_A_pcom, course_hours, sched)

    if (len(term_B_pcom) > 0):
        sched = add_courses(term_B_pcom, course_hours, sched)

    if (len(term_A_bcom) > 0):
        sched = add_courses(term_A_bcom, course_hours, sched)

    if (len(term_B_bcom) > 0):
        sched = add_courses(term_B_bcom, course_hours, sched)

    return sched


def update_schedule(course_hours: Dict[str, int], prev_sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the previous day's schedule and the course hours dict. If any courses
    have met their term hour requirements, they are removed and replaced with empty strings
    '''
    
    # courses that have met their required hours should be removed
    finished_courses = [course_id for course_id in course_hours if 
                        course_hours[course_id]['remaining'] <= 0]
            
    for (index, time) in prev_sched.iterrows():
        for room in prev_sched.columns:
            if time[room][:-2] in finished_courses:
                prev_sched.loc[index, room] = ""
        
    return prev_sched



def add_courses(courses: List[Course],
                course_hours: Dict[str, int], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    For each unscheduled course, check if there is enough room for all cohorts.
    If there is,update the schedule before moving to the next course.
    A course is only added if there is room for all cohorts
    '''

    for course in courses:

        if (course.isOnline or course.hasLab):
            continue

        # list of tuples used to add course to the schedule if space is found
        # each tuple corresponds to (room index, time slot index) for a given cohort
        cohort_indexes = []
        
        hours_left = course_hours[course.ID]['remaining']
        if (hours_left >= course.duration):
            blocks = int(course.duration // 0.5)
        else:
            blocks = math.ceil(hours_left / 0.5)

        # size of schedule opening required to fit current course
        required_gap = np.array([""] * blocks)
        
        # number of schedule gaps that will fit current course (need enough for all cohorts)
        count = 0
        
        # count the number of non-overlapping occurances of `required_gap` in each room
        for (room_name, time_slots) in sched.items():
            left = 0
            right = len(required_gap)
            while (right < len(time_slots.values) + 1):

                if np.array_equal(time_slots.values[left:right], required_gap):
                    cohort_indexes.append( (sched.columns.get_loc(room_name), left) )
                    left = right
                    right += len(required_gap)
                    count += 1
                else:
                    left += 1
                    right += 1

        if count >= COHORT_COUNT:
            sched = add_course_cohorts(course, blocks, cohort_indexes, sched)

    return sched    


def add_course_cohorts(course: Course, blocks: int,
                       cohort_indexes: List[Tuple[int, int]], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes a list of Courses and adds each one to the schedule at the earliest 
    available time & room (if possible). Repeats until all
    cohorts have been added, or the schedule is completely full.
    '''

    cohort_IDs = string.ascii_uppercase[:COHORT_COUNT]

    # each course instance needs to appear once for every cohort
    for i in range(len(cohort_IDs)):

        course_id = course.ID
        cohort_ID = cohort_IDs[i]
        course_strs = [course_id + "-" + cohort_ID] * blocks
        room_index, start_time = cohort_indexes[i]

        sched.iloc[start_time:(start_time + blocks), room_index] = course_strs

    return sched


def add_labs(lectures: Dict[str, List[Course]], labs: Dict[str, List[Course]],
             lab_hours: Dict[str, int],lab_col: pd.DataFrame, 
             sched: pd.DataFrame, term: int) -> pd.DataFrame:
    
    # bcom has no labs
    filtered_pcom_A = [l for l in labs['pcom']['term A'] 
                       if (lab_hours[l.ID])['remaining'] > 0]
    filtered_pcom_B = [l for l in labs['pcom']['term B'] 
                       if (lab_hours[l.ID])['remaining'] > 0]
    
    lab_ID_dict = {
        'pcom A': [c.ID for c in labs['pcom']['term A']],
        'pcom B': [c.ID for c in labs['pcom']['term B']],
    }
    
    lec_ID_dict = {
        'pcom A': [c.ID for c in lectures['pcom']['term A']],
        'pcom B': [c.ID for c in lectures['pcom']['term B']],

    }
    
    transposed_lecs = sched.T
    
    booked_times = {}
    for time in transposed_lecs.columns:
        booked_times[time] = transposed_lecs[time].tolist()
        
    for time in lab_col.rows():
        pcom_A_scheduled = [course[:-2] for course in booked_times[time] 
                            if course in lec_ID_dict['pcom A']]
        pcom_B_scheduled = [course[:-2] for course in booked_times[time] 
                            if course in lec_ID_dict['pcom B']]
        
        for lab in labs['pcom']['term A']:
            if (pcom_A_scheduled.count(lab.ID) >= COHORT_COUNT):
                continue
            
            if lab in filtered_pcom_A:
                schedule_lab(lab_col, lab, booked_times, time, lab_hours)
            

def schedule_lab(lab_col: pd.DataFrame, lab: Course, booked: Dict[str, List[str]], 
                 start: str, lab_hours: Dict[str, int]) -> pd.DataFrame:
    
    
    return lab_col

def find_lab_opening(booked_times: Dict[str, List[str]], time: str) -> List[str]:
    
    
    
    return ['A', 'B', 'C', 'D']




def create_core_term_schedule(lectures: Dict[str, List[Course]], labs: Dict[str, List[Course]],
                              rooms: List[Classroom], term: int) -> List[pd.DataFrame]:
    '''
    Main schedule creation function that makes 26 single-day schedules (mon/wed, 13 weeks)
    each as a pandas DataFrame, and returns them in a list
    '''
    term_A_pcom_lecs = lectures['pcom']['term A']
    term_B_pcom_lecs = lectures['pcom']['term B']
    
    term_A_pcom_labs = labs['pcom']['term A']
    term_B_pcom_labs = labs['pcom']['term B']
    
    term_A_bcom_lecs = lectures['bcom']['term A']
    term_B_bcom_lecs = lectures['bcom']['term B']

    term_A_bcom_labs = labs['bcom']['term A']
    term_B_bcom_labs = labs['bcom']['term B']

    lec_hours = get_course_hours((term_A_pcom_lecs + term_B_pcom_lecs +
                                  term_A_bcom_lecs + term_B_bcom_lecs))
    
    lab_hours = get_course_hours((term_A_pcom_labs + term_B_pcom_labs +
                                  term_A_bcom_labs + term_B_bcom_labs))

    # create schedules for the first day, then reference this when making 
    # subsequent schedules to get consistent times and rooms for courses
    prev_lecs = create_empty_schedule([room for room in rooms if not room.isLab])
    prev_labs = create_empty_schedule([room for room in rooms if room.isLab])
    
    temp_sched_arr = []
    day = 1

    while day < 27:
        
        lecture_sched = make_lecture_schedule(
            term_A_pcom_lecs, term_B_pcom_lecs,
            term_A_bcom_lecs, term_B_bcom_lecs,
            lec_hours, prev_lecs
        )
        
        lab_column = create_empty_schedule([room for room in rooms if room.isLab])
        
        full_schedule = add_labs(
            lectures, labs, lab_hours, lab_column, lecture_sched, term
        )
        
        
        lec_hours = update_course_hours(lec_hours, lecture_sched)
        prev_lecs = update_schedule(lec_hours, lecture_sched)
        
        print(f"\n\n\t\tDAY {day}: \n{lecture_sched}")
        day += 1
        
        continue
        
        
        partial_sched  = add_lab_schedule(
            term_A_pcom_labs, term_B_pcom_labs,
            term_A_bcom_labs, term_B_bcom_labs,
            lab_hours, prev_labs, day, lecture_sched
        )
        
        # store the combined schedules as an immutable static frame to prevent weird bug
        # where schedules end up empty after this loop ends (no idea why this happens,
        # but good luck to whoever has to sort through this mess & find an actual solution)
        temp_sched_arr.append(sf.Frame.from_pandas(sched))

        course_hours = update_course_hours(course_hours, sched)
        prev_sched   = update_schedule(course_hours, sched)
        
        day += 1
    
    # convert each static frame back to a dataframe & return them in a list
    full_schedule = []
    for sf_sched in temp_sched_arr:
        full_schedule.append(sf_sched.to_pandas())
        
    return full_schedule
