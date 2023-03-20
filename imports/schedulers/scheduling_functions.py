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
from itertools import chain, permutations
from more_itertools import chunked
from typing import *


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

#===================== TODOs (in no particular order) ==========================

# TODO: if there are 5 cohorts, cohorts A and E should have their hours updated properly

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


# assuming ~130-150 new students/term requires 4 different lecture groups for each course
COHORT_COUNT = 4
# ==============================================================================

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
        sched[room.ID] = [""] * 19

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

            # remove cohort identifier
            course_name = course[:-2]

            if course[:-2] in seen:
                continue

            seen.add(course[:-2])
            
            scheduled_hours = (courses.count(course)) * 0.5
                
            course_hours[course_name]['scheduled'] += scheduled_hours
            course_hours[course_name]['remaining'] -= scheduled_hours

    return course_hours

def get_lab_cohorts():
    cohort_IDs = [c for c in string.ascii_uppercase[:COHORT_COUNT]]

    # only 1 lab room means we can only schedule 4 cohorts on each day
    # cohorts A and E will have to alternate
    if COHORT_COUNT > 4:
        mon_cohorts = cohort_IDs[:-1]
        wed_cohorts = cohort_IDs[1:]
        
    else:
        mon_cohorts = wed_cohorts = cohort_IDs
        
    return [mon_cohorts, wed_cohorts]

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
    
    # labs can only hold 4 cohorts, if we have 5 then alternate cohorts A and E 
    # after each day
    if COHORT_COUNT > 4 and prev_sched.columns[0].endswith("(LAB)"):
        for index, time in enumerate(prev_sched.index):
            
            if prev_sched.iloc[index, 0].endswith("A"):
                prev_sched.iloc[index, 0] = prev_sched.iloc[index, 0][:-1] + "E"
                
            elif prev_sched.iloc[index, 0].endswith("E"):
                prev_sched.iloc[index, 0] = prev_sched.iloc[index, 0][:-1] + "A"

    for time in prev_sched.index:
        for room in prev_sched.columns:
            if prev_sched.loc[time, room][:-2] in finished_courses:
                prev_sched.loc[time, room] = ""

    return prev_sched

def add_courses(courses: List[Course], 
                course_hours: Dict[str, int], sched: pd.DataFrame) -> pd.DataFrame:
    '''
    For each unscheduled course, check if there is enough room for all cohorts.
    If there is, update the schedule before moving to the next course.
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
             course_hours: Dict[str, int], cohorts: List[str], lab_col: pd.DataFrame, 
             sched: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes the existing lecture schedule and information on what labs to schedule,
    and checks at each row (time) if a lab can be scheduled without any conflicts
    '''
    
    # bcom has no labs
    filtered_pcom_A = [l for l in labs['pcom']['term A'] 
                       if (course_hours[l.ID])['remaining'] > 0]
    filtered_pcom_B = [l for l in labs['pcom']['term B'] 
                       if (course_hours[l.ID])['remaining'] > 0]
    
    filtered_pcom_A.sort(key=lambda x: x.termHours)
    filtered_pcom_B.sort(key=lambda x: x.termHours)
    
    lec_ID_dict = {
        'pcom A': [c.ID for c in lectures['pcom']['term A']],
        'pcom B': [c.ID for c in lectures['pcom']['term B']],
    }
    
    transposed_lecs = sched.T
    booked_pcom = {'pcom A': {}, 'pcom B': {}}
    
    for index, time in enumerate(list(transposed_lecs.columns)):
        
        pcom_A = [course for course in transposed_lecs[time].tolist() if
                  course[:-2] in lec_ID_dict['pcom A']]
        
        pcom_B = [course for course in transposed_lecs[time].tolist() if
                  course[:-2] in lec_ID_dict['pcom B']]
        
        booked_pcom['pcom A'][index] = pcom_A
        booked_pcom['pcom B'][index] = pcom_B
        
        
    for i in range(len(lab_col.index)):
        for lab in filtered_pcom_A:
            if (len(booked_pcom['pcom A'][i]) >= len(cohorts)):
                continue
            lab_col = schedule_lab(
                lab_col, lab, cohorts, booked_pcom['pcom A'], i, course_hours
            )
             
        for lab in filtered_pcom_B:
            if (len(booked_pcom['pcom A'][i]) >= len(cohorts)):
                continue
            lab_col = schedule_lab(
                lab_col, lab, cohorts, booked_pcom['pcom B'], i, course_hours
            )
                
    return lab_col

            
def schedule_lab(lab_col: pd.DataFrame, lab: Course, cohorts: List[str], 
                 booked_lecs: Dict[int, List[str]], start: int, lab_hours: Dict[str, int]) -> pd.DataFrame:
    '''
    Checks the lecture schedule `booked` to see if a given lab can be scheduled 
    without any conflicts. Courses are scheduled with each cohort one after the other
    '''

    hours_left = lab_hours[lab.ID]['remaining']
    
    if (hours_left >= lab.duration):
        blocks = int(lab.duration // 0.5)
    else:
        blocks = math.ceil(hours_left / 0.5)
        
    required_gap = np.array([""] * blocks * len(cohorts))
    
    # use a sliding window to find an available time
    left  = start
    right = left + len(required_gap)
    
    while (right < len(lab_col.index) + 1):    
        curr_gap = lab_col.iloc[left:right, 0]
        
        # open time slot found
        if np.array_equal( np.array(curr_gap.values), required_gap ):
            cohort_order = find_lab_opening(booked_lecs, left, blocks, cohorts)
            # cohorts can be assigned without any conflicts with lecture times
            if (len(cohort_order) != 0):         
                break
        left += 1
        right += 1
        
    # only executes if we checked all the lab times without finding an open slot
    else:
        return lab_col
        
    # update and return new lab schedule
    lab_cohorts = []
    for cohort in cohort_order:
        lab_cohort_strs = [lab.ID + '-' + cohort] * blocks
        lab_cohorts.extend(lab_cohort_strs)
        
    lab_col.iloc[left:right, 0] = lab_cohorts
    
    return lab_col


def find_lab_opening(booked_lecs: Dict[int, List[str]], start: int, 
                     blocks: int, cohorts: List[str]) -> List[str]:
    '''
    Compares a possible start & end time for a lab and returns the order in which
    cohorts should be assigned without conflicting with the lecture schedule.
    Returns an empty list if no combination is possible
    '''
    
    booked_cohorts = {}
    for i in range(blocks):
        booked_cohorts[i] = []
        block_start = start+(blocks*i)
        block_end = min(block_start+blocks, 19)
        
        for j in range(block_start, block_end):
            curr_IDs = [s[-1] for s in booked_lecs[j] if s[-1] not in booked_cohorts[i]]
            booked_cohorts[i].extend(curr_IDs)


    for invalid_ID_list in booked_cohorts.values():
        if len(invalid_ID_list) >= COHORT_COUNT:
            return []
    
    # remove invalid cohort permutations from list of all possible permutations
    perms = list(permutations(cohorts))
    valid = [list(p) for p in perms]
    
    for i in range(len(cohorts)):
        for p in perms:
            if (i >= len(booked_cohorts.keys())):
                continue
            if p[i] in booked_cohorts[i] and list(p) in valid:
                valid.remove(list(p))
    
    return valid[0] if len(valid) > 0 else []


def create_core_term_schedule(lectures: Dict[str, List[Course]], labs: Dict[str, List[Course]],
                              rooms: List[Classroom]) -> List[pd.DataFrame]:
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
    
    course_hours = get_course_hours((term_A_pcom_lecs + term_B_pcom_lecs +
                                     term_A_bcom_lecs + term_B_bcom_lecs + 
                                     term_A_pcom_labs + term_B_pcom_labs +
                                     term_A_bcom_labs + term_B_bcom_labs))

    # create schedules for the first day, then reference this when making 
    # subsequent schedules to get consistent times and rooms for courses
    prev_lecs = create_empty_schedule([room for room in rooms if not room.isLab 
                                       and not room.ID.startswith('ONLINE')])
    prev_labs = create_empty_schedule([room for room in rooms if room.isLab])
    
    mon_lab_cohorts, wed_lab_cohorts = get_lab_cohorts()
    
    temp_sched_arr = []
    day = 1

    while day < 27:
        
        lecture_sched = make_lecture_schedule(
            term_A_pcom_lecs, term_B_pcom_lecs,
            term_A_bcom_lecs, term_B_bcom_lecs,
            course_hours, prev_lecs
        )
        
        if (day % 2 == 0):
            lab_sched = add_labs(
                lectures, labs, course_hours, 
                wed_lab_cohorts, prev_labs, lecture_sched
        )
        else:
            lab_sched = add_labs(
                lectures, labs, course_hours, 
                mon_lab_cohorts, prev_labs, lecture_sched
        )
        
        joined_sched = lecture_sched.join(lab_sched)
        
        # store the combined schedules as an immutable static frame to 
        # prevent weird bug where schedules get messed up after this loop ends
        # (no idea why this happens, but good luck to whoever works on this next)
        temp_sched_arr.append(sf.Frame.from_pandas(joined_sched))
        
        course_hours = update_course_hours(course_hours, lecture_sched)
        course_hours = update_course_hours(course_hours, lab_sched)
        
        prev_lecs = update_schedule(course_hours, lecture_sched)
        prev_labs = update_schedule(course_hours, lab_sched)

        day += 1
        
    
    # convert each static frame back to a dataframe & return them in a list
    full_schedule = {}
    for day, sf_sched in enumerate(temp_sched_arr):
        full_schedule[f"day {day+1}"] = (sf_sched.to_pandas())
        
    print(course_hours)
    return full_schedule
