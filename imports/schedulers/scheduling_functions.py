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

#TODO: create second df for scheduling labs, join lecture & lab dfs after each 'day' iteration


#TODO: get actual cohort count from fillClassrooms.py, make sure this stuff works for any number of cohorts


#TODO: check for holidays (might be easier if we use date objects rather than day 1, day 2, etc.) 

#TODO: create lecture objects either:
#           - after the schedule is made, or
#           - before: store each lecture's ID in the dataframe & update it's hours when it gets added to the schedule


# assuming ~100-120 new students/term requires 4 different lecture groups for each course
COHORT_COUNT = 4
# ==============================================================================
# NOT BEING USED
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

# NOT BEING USED
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

# NOT BEING USED
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

#NOT BEING USED
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

#NOT BEING USED
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

    for room in (room_list):
        if (room.isLab):
            sched[f"{room.ID} (LAB)"] = [""] * 19
        else:
            sched[room.ID] = [""] * 19

    return sched


def get_course_hours(lectures: List[Course], labs: List[Course]) -> Tuple[Dict[str, int], Dict[str, int]]:
    '''
    Create 2 dictionaries that will be used to keep track of how many hours
    a given course has, and how many hours it has left. One dictionary handles
    lecture hours, the other handles lab hours 
    '''
    lecture_hours = {}
    lab_hours = {}

    for course in lectures:
        lecture_hours[course.ID] = {
            'required': course.termHours,
            'remaining': course.termHours,
            'scheduled': 0,
        }

    for course in labs:
        lab_hours[course.ID] = {
            'required': course.termHours,
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

def create_core_day_schedule(term_A_pcom: List[Course], term_B_pcom: List[Course], 
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
    
    # for each term/program, get a list of the courses that can be scheduled in a 
    # given room on a single day. Each course list is unique, so we dont need to 
    # update course_hours between any of these calls
    if (len(term_A_pcom) > 0):
        sched = add_course_cohorts_to_sched(term_A_pcom, course_hours, sched)
    
    if (len(term_B_pcom) > 0):
        sched = add_course_cohorts_to_sched(term_B_pcom, course_hours, sched)
    
    if (len(term_A_bcom) > 0):
        sched = add_course_cohorts_to_sched(term_A_bcom, course_hours, sched)
    
    if (len(term_B_bcom) > 0):
        sched = add_course_cohorts_to_sched(term_B_bcom, course_hours, sched)

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


def add_course_cohorts_to_sched(courses: List[Course], course_hours: Dict[str, int], 
                                sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes a list of courses that haven't been scheduled yet and the current schedule.
    For each course, we check if there is enough room for all cohorts.
    If there is, we update the schedule accordingly before moving to the next course.
    '''
    
    for course in courses:
        
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
            
        # if we have enough room for the current course & all its cohorts,
        # append the course to the schedule before the next iteration so we dont
        # use the same schedule gap again
        if count >= COHORT_COUNT:
            sched = add_lec_to_core_schedule(course, blocks, cohort_indexes, sched)
          
    return sched    

def add_lec_to_core_schedule(course: Course, blocks: int, 
                             cohort_indexes: List[Tuple[int,int]], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes a list of Courses and adds each one to the schedule at the earliest 
    available time & room (if possible). This process repeats until all
    cohorts have been added, or the schedule is completely full.
    '''
    
    cohort_IDs = string.ascii_uppercase[:COHORT_COUNT]
    
    # each course instance needs to appear once for every cohort
    for i in range(len(cohort_IDs)):
        course_id   = course.ID
        cohort_ID   = cohort_IDs[i]
        course_strs = [course_id + "-" + cohort_ID] * blocks
        room_index, start_time = cohort_indexes[i]
        
        sched.iloc[start_time:(start_time + blocks), room_index] = course_strs
            
    return sched
    

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

    temp_sched_arr = []
    
    # create a schedule for the first day, then reference this when making 
    # subsequent schedules with consistent times and rooms for courses
    prev_sched = create_empty_schedule(lecture_rooms)
    
    for i in range(1, 27):
        
        sched = create_core_day_schedule(
            term_A_pcom, term_B_pcom,
            term_A_bcom, term_B_bcom,
            lecture_hours, prev_sched
        )
        
        # only add immutable static frames, otherwise all the schedules end up empty 
        # (no idea why, but good luck to whoever has to sort through this mess & find an actual solution)
        temp_sched_arr.append(sf.Frame.from_pandas(sched))
        
        lecture_hours = update_course_hours(lecture_hours, sched)
        prev_sched = update_schedule(lecture_hours, sched)
        
    
    # convert each static frame back to a dataframe & return them in a dict
    full_schedule = {}
    for index, sf_sched in enumerate(temp_sched_arr):
        full_schedule[f"day {index+1}"] = sf_sched.to_pandas()
        
    return full_schedule
