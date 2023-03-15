import os, sys
import math
import datetime
import pprint
import pandas as pd
import numpy as np
from imports.classes.courses import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
import string
from typing import *
from itertools import cycle

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

#===================== TODOs (in no particular order) ==========================

#TODO: Schedule pcom_0130 & pcom_0140 halfway through term

#TODO: after the entire schedule is made, assign times to online classes (e.g. AVDN 0260)
#           - use seperate dataframe or dict, while still watching out for schedule conflicts
#           - constraints: no student limit, cant be within 1.5 hours of an in-person class
#TODO: schedule more than 1 course in a given room each day 


#TODO: get actual cohort count from fillClassrooms.py, make sure this stuff works for any number of cohorts


#TODO: try to leave courses with a consistent starting time, rather than moving
#      them around when another course is removed from the schedule

#TODO: check for holidays (might be easier if we use date objects rather than day 1, day 2, etc.) 

#TODO: create lecture objects either:
#           - after the schedule is made, or
#           - before: store each lecture's ID in the dataframe & update it's hours when it gets added to the schedule


# assuming ~100-120 new students/term requires 4 different lecture groups for each course
COHORT_COUNT = 4
# ==============================================================================
def cohort_id_generator():
    '''
    Generator that yield a list of cohort IDs (Capital letters starting at A)
    After each call the list is shifted (the last element is moved to the front)
    This prevent scheduling conflicts for cohort groups
    '''   
    cohortIDs = list(string.ascii_uppercase[:COHORT_COUNT])
    while True:
        yield cohortIDs
        cohortIDs = [cohortIDs[-1]] + cohortIDs[:-1]
        
        
def create_empty_schedule(room_list: List[Classroom]) -> pd.DataFrame:
    '''
    This function creates an empty pandas dataframe to represent the schedule 
    for a single day. The column headers are room numbers and the row indexes 
    are times (half hour increments)
    '''

    # 8 AM - 5 PM in half-hour increments 
    times = [datetime.time(i, j).strftime("%H:%M") for i in range (8, 17) for j in [0, 30]]
    times.append(datetime.time(17, 0).strftime("%H:%M"))
    
    sched = pd.DataFrame(index = times)
    
    for room in (room_list):
        if (room.isLab):
            sched[f"{room.ID} (LAB)"] = [""] * 19
        else:
            sched[room.ID] = [""] * 19
        
    return sched

def get_course_hours(lectures: List[Course], labs: List[Course]) -> Tuple[Dict[str,int], Dict[str,int]]:
    '''
    Create 2 dictionaries that will be used to keep track of how many hours
    a given course has, and how many hours it has left. One dictionary handles
    lecture hours, the other handles lab hours 
    '''
    lecture_hours = {}
    lab_hours     = {}
    
    for course in lectures:
        lecture_hours[course.ID] = {
            'required' : course.termHours, 
            'remaining': course.termHours,
            'scheduled': 0, 
    }
        
    for course in labs:
        lab_hours[course.ID] = {
            'required' : course.termHours, 
            'remaining': course.termHours,
            'scheduled': 0, 
    }
        
    return lecture_hours, lab_hours

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

def create_day_schedule(course_hours: Dict[str, int], course_list: List[Course], room_list: List[Classroom]) -> pd.DataFrame:
    '''
    This function takes an empty dataframe representing the schedule for a given day,
    and adds 3 cohorts for each course, starting with the ones that have 
    the most term hours. To prevent scheduling conflicts, each course is limited to 1 room only
    '''
    
    sched = create_empty_schedule(room_list)

    # ignore courses that have been fully scheduled
    course_list = [course for course in course_list if 
                   course_hours[course.ID]['remaining'] > 0]
        
    # sort course_list by required term hours (descending)
    course_list.sort(key=lambda x: x.termHours, reverse=True)

    # schedule online courses first
    for index, room in enumerate(room_list):
        # if all courses have been scheduled, leave the leftover rooms empty
        if (index >= len(course_list)):
            break
        
        if room.isLab:
            room_col_index = sched.columns.get_loc(room.ID + " (LAB)")
        else:
            room_col_index = sched.columns.get_loc(room.ID)
            
        curr_course = course_list[index]

        hours_left = course_hours[curr_course.ID]['remaining']
        duration   = curr_course.duration

        # try to schedule course for it's specified duration
        if (hours_left >= duration):
            # number of half-hour blocks that room is booked for
            blocks = int(duration // 0.5)
        else:
            # round up to the nearest half-hour
            blocks = math.ceil(hours_left / 0.5)

        # add identifiers to differentiate cohorts
        # (needs fixing: see TODOs at the top)
        cohort_IDs = next(id_generator)
        cohorts = []
        for id in cohort_IDs:
            cohort_str = curr_course.ID + "-" + id
            cohorts.extend([cohort_str] * blocks)
            
        # to prevent schedule conflicts, put lectures in the morning and labs in the evening
        # TODO: schedule online courses in the most available room (in the evening)
        if room.isLab or curr_course.isOnline:
            sched.iloc[-(blocks*COHORT_COUNT):, room_col_index] = cohorts
        else:
            sched.iloc[:(blocks*COHORT_COUNT), room_col_index] = cohorts

    return sched

def create_term_schedule(lecture_hours: Dict[str, int], lectures: List[Course], lecture_rooms: List[Classroom], 
                         lab_hours: Dict[str, int], labs: List[Course], lab_rooms: List[Classroom]) -> Dict[str, pd.DataFrame]:
    '''
    Main schedule creation function that makes 26 single-day schedules (monday & wednesday, 13 weeks)
    Lecture & Lab schedules are done seperately (easier to keep track of rooms this way), 
    then joined into a single dataframe and stored in a dictionary. To make things easier, 
    if the new schedule is the same as the previous day, '-' is added to the dict as a placeholder
    '''
    
    full_schedule = {}
    global id_generator
    id_generator = cohort_id_generator()
    for i in range(1, 27):

        lecture_sched = create_day_schedule(lecture_hours, lectures, lecture_rooms)
        lecture_hours = update_course_hours(lecture_hours, lecture_sched)

        lab_sched = create_day_schedule(lab_hours, labs, lab_rooms)
        lab_hours = update_course_hours(lab_hours, lab_sched)

        full_day_sched = lecture_sched.join(lab_sched)
        
        # add place holders to `full_schedule` dict to avoid duplicates
        # TODO: try to find a way to check if the new schedule will be a duplicate of the previous one
        #       before calling the above functions
        if any(full_day_sched.equals(day_sched) for day_sched in list(full_schedule.values())):
            full_schedule[f"day {i}"] = "-"
            
        else:
            full_schedule[f"day {i}"] = full_day_sched      

    
    return full_schedule

def validate_sched(full_schedule: Dict[str, pd.DataFrame]) -> bool:
    '''
    Takes the full term's schedule as a dictionary and checks that there are no 
    scheduling conflicts (i.e. no cohort group is booked to 2 rooms at the same time)
    '''
    for day_num, sched in full_schedule.items():
        # transpose schedule
        # iterate time slots (now columns):
        #   - create a list of cohorts scheduled in each room at curr_time_slot (e.g. pcom term 1 grpup A)
        #   - if any group appears more than once, return false
        pass
    
    return True


def get_available_time(room_sched: List[str], blocks: int) -> int:
    '''
    Helper function that checks if a room is available for a specific time period
    on a given day. Returns the starting index (time) of when the room becomes
    available. If no availability is found, returns -1
    '''
    # number of time blocks required to fit lecture into schedule
    available= [""] * blocks

    start = 0
    end   = blocks
    while (end < len(room_sched) + 1):    
        if room_sched[start:end] == available:
            return start 
        start += 1
        end += 1
    
    return -1


def create_core_lec_schedule(term_A_pcom: List[Course], term_B_pcom: List[Course], 
                             term_A_bcom: List[Course], term_B_bcom: List[Course],
                             course_hours: Dict[str, int], room_list: List[Classroom]) -> pd.DataFrame:
    
    '''
    Takes lists of pcom & bcom lectures for terms A & B, a dictionary of course_hours, 
    and a room list to create a schedule for a single day and return it as a 
    DataFrame. Courses are scheduled by pcom/bcom and term, moving from rooms
    left to right, starting at 8 am, where each cohort takes up half a day.
    '''

    sched = create_empty_schedule(room_list)
    
    # ignore courses that have been fully scheduled
    term_A_pcom = [course for course in term_A_pcom if
                   course_hours[course.ID]['remaining'] > 0]
    term_B_pcom = [course for course in term_B_pcom if
                   course_hours[course.ID]['remaining'] > 0]
    term_A_bcom = [course for course in term_A_bcom if
                   course_hours[course.ID]['remaining'] > 0]
    term_B_bcom = [course for course in term_B_bcom if
                   course_hours[course.ID]['remaining'] > 0]
    
    # sort courses by required hours in descending order
    term_A_pcom.sort(key=lambda x: x.termHours, reverse=True)
    term_B_pcom.sort(key=lambda x: x.termHours, reverse=True)
    term_A_bcom.sort(key=lambda x: x.termHours, reverse=True)
    term_B_bcom.sort(key=lambda x: x.termHours, reverse=True)
    
    # for each term/program, get a list of the courses that can be scheduled in a 
    # given room on a single day
    curr_term_A_pcom = get_courses_to_schedule(term_A_pcom)
    curr_term_B_pcom = get_courses_to_schedule(term_B_pcom)
    curr_term_A_bcom = get_courses_to_schedule(term_A_bcom)
    curr_term_B_bcom = get_courses_to_schedule(term_B_bcom)
    
    # each list has unique courses, so we dont need to update course_hours between these calls
    sched = append_lec_to_core_schedule(curr_term_A_pcom, course_hours, sched)
    sched = append_lec_to_core_schedule(curr_term_B_pcom, course_hours, sched)
    sched = append_lec_to_core_schedule(curr_term_A_bcom, course_hours, sched)
    sched = append_lec_to_core_schedule(curr_term_B_bcom, course_hours, sched)

    return sched

def get_courses_to_schedule(courses: List[Course]) -> List[Course]:
    '''
    Takes a list of courses sort by required hours in descending order, and 
    returns a list of the first n courses that will fit in a single day's schedule,
    assuming that each day will need to fit in 2 cohorts.
    '''
    # number of hours in a single day's schedule
    max_hours  = 9
    curr_total = 0
    can_schedule = []

    for course in courses:
        # multiply by 2 to account for 2 cohorts/day
        if ((curr_total + (course.duration * 2)) > max_hours):
            return can_schedule
        curr_total += (course.duration * 2)
        can_schedule.append(course)
    
    return can_schedule

def append_lec_to_core_schedule(courses: List[Course], course_hours: Dict[str, int], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes a list of Courses and adds each one to the schedule at the earliest 
    available time & room (see get_start_time). This process repeats until all
    cohorts have been added, or the schedule is completely full.
    '''
    
    cohort_IDs = cycle(string.ascii_uppercase[:COHORT_COUNT])
    
    # each course instance needs to appear once for every cohort
    for i in range(COHORT_COUNT):
        curr_cohort = next(cohort_IDs)
        for course in courses:
            course_id  = course.ID
            duration   = course.duration
            hours_left = course_hours[course_id]['remaining']
            
            # try to schedule course for it's specified duration
            if (hours_left >= duration):
                # number of half-hour blocks that the course will take up
                blocks = int(duration // 0.5)
            else:
                # round up to the nearest half-hour
                blocks = math.ceil(hours_left / 0.5)
                
            course_str = [course_id + "-" + curr_cohort] * blocks
            room_index, start_time = find_available_time(sched, blocks)
            
            if room_index == -1: continue
            
            sched.iloc[start_time:(start_time + blocks), room_index] = course_str
            
    return sched


def find_available_time(sched: pd.DataFrame, blocks: int) -> Tuple[int, int]:
    '''
    Takes the current schedule for a single day and the number of half-hour blocks
    a course should be scheduled for. Returns a tuple of the room column index and the 
    starting time index for the earliest available time slot for the course
    Returns -1 if no available time is found.
    '''
    # number of time blocks required to fit lecture into schedule
    available = [""] * blocks
    
    for (room_name, time_slots) in sched.items():
        start = 0
        end   = blocks 
        while (end < len(time_slots.values) + 1):
            if np.array_equal(time_slots.values[start:end], available):
                return (sched.columns.get_loc(room_name), start)
            start += 1
            end += 1

    return (-1, -1)
    

def create_core_term_schedule(term_A_pcom: List[Course], term_B_pcom: List[Course],
                              term_A_bcom: List[Course], term_B_bcom: List[Course], 
                              lecture_rooms: List[Classroom]) -> Dict[str, pd.DataFrame]:
    '''
    Main schedule creation function that makes 26 single-day schedules (monday & wednesday, 13 weeks)
    Lecture & Lab schedules are done seperately (easier to keep track of rooms this way), 
    then joined into a single dataframe and stored in a dictionary. To make things easier, 
    if the new schedule is the same as the previous day, '-' is added to the dict as a placeholder
    '''
    all_lectures = term_A_pcom + term_B_pcom + term_A_bcom + term_B_bcom 

    lecture_hours, lab_hours = get_course_hours(all_lectures, [])

    full_schedule = {}
    
    for i in range(1, 27):
        
        sched = create_core_lec_schedule(
            term_A_pcom, term_B_pcom, 
            term_A_bcom, term_B_bcom, 
            lecture_hours, lecture_rooms
        )
        
        lecture_hours = update_course_hours(lecture_hours, sched)
        
        # removing duplicate schedules makes debugging much easier
        if any(sched.equals(day_sched) for day_sched in list(full_schedule.values())):
            full_schedule[f"day {i}"] = "-"
        else:
            full_schedule[f"day {i}"] = sched

    return full_schedule
