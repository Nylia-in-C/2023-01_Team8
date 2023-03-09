import os, sys
import math
import datetime
import pprint
import pandas as pd
from imports.classes.courses import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
import string
from typing import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

#TODO: Schedule pcom_0130 halfway through term
#TODO: Schedule pcom_0140 halfway through term
#TODO: Schdeule avdm_0260



# assuming ~70-90 new students/term requires 3 different lecture groups for each course
COHORT_COUNT = 3
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
        # using a generator to shift the cohort groups will prevent scheduling conflicts
        # TODO: add checking for edge case: 
        #          This wont prevent scheduling conflicts if theres only 1 or 2 cohorts 
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


 # not being used, but we might need this in the future
# def get_available_time(room_sched, blocks):
#     '''
#     Helper function that checks if a room is available for a specific time period
#     on a given day. Returns the starting index (time) of when the room becomes
#     available. If no availability is found, returns -1
#     '''
#     # number of time blocks required to fit lecture into schedule
#     available= [""] * blocks

#     start = 0
#     end   = blocks
#     while (end < len(room_sched) + 1):    
#         if room_sched[start:end] == available:
#             return start 
#         start  += 1
#         end += 1
    
#     return -1

if __name__ == '__main__':

    
    print("Enter a number for the term you want to generate a schedule for: \
          \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    print("Enter a number for the Core Courses Schedule or the Program Schedule: \
          \n1. Core \n2. Program")
    CoreOrProgram = int(input())
    
    if CoreOrProgram == 1:
        print("==========================Monday Wednesday==========================")

        # schedule lectures & labs seperately
        lectures = [course for course in term_courses[term] if course not in lab_courses]
        labs     = [course for course in term_courses[term] if course in lab_courses]
        
        lecture_hours, lab_hours = get_course_hours(lectures, labs)
        
        full_schedule = create_term_schedule(lecture_hours, lectures, lecture_rooms, lab_hours, labs, lab_rooms)

        
        for day, sched in full_schedule.items():
            if not (isinstance(sched, str)):
                print(f"\n\n{day}: \n {sched}")
    
    if CoreOrProgram == 2:
        print("==========================Tuesday Thursday==========================")

        # Program schedule
        # program-lectures
        program_lectures = [course for course in program_term_courses[term] if course not in program_lab_courses]
        # program-hours
        program_labs     = [course for course in program_term_courses[term] if course in program_lab_courses]

        program_lecture_hours, program_lab_hours = get_course_hours(program_lectures, program_labs)

        program_full_schedule = create_term_schedule(program_lecture_hours, program_lectures, lecture_rooms, program_lab_hours, program_labs, lab_rooms)

        for day, sched in program_full_schedule.items():
            if not (isinstance(sched, str)):
                print(f"\n\n{day}: \n {sched}")
    
    #Notes:
    #   - Classes don't have a consistent starting time. When classes drop out of the schedule they get shifted up.
    #   - Only one course is scheduled per room per day. Most impactful for labs, lots of empty space where labs could squeeze

    #TODO: 
    #   - write function to validate no scheduling conflicts (no 'horizontal' overlap between cohorts)
    #   - initialize course & classroom objects in seperate file
    #   - create lecture objects rather than creating/displaying dataframe (maybe)

