# import os, sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# grandparentdir = os.path.dirname(parentdir)
# sys.path.append(grandparentdir)

import math
import datetime
import pprint
import pandas as pd
from imports.classes.courses import *
from imports.classes.classrooms import *
import string
from typing import *

#initialize objects/dummy data==================================================

# Core Courses------------------------------------------------------------------

# term 1 PCOM core courses
pcom_0101 = Course('PCOM 0101', 'Business Writing 1', 35, 1.5, True, False, False)
pcom_0105 = Course('PCOM 0105', 'Intercultural Communication Skills', 35, 1.5, True, False, False)
pcom_0107 = Course('PCOM 0107', 'Tech Development 1', 18, 2, True, False, False)
cmsk_0233 = Course('CMSK 0233', 'MS Project Essentials', 7, 2, True, False, False)
cmsk_0235 = Course('CMSK 0235', 'MS Visio Essentials', 6, 2, True, False, False)

# term 2 PCOM core courses
pcom_0102 = Course('PCOM 0102', 'Business Writing 2', 35, 1.5, True, False, False)
pcom_0201 = Course('PCOM 0201', 'Fundamentals of Public Speaking', 35, 1.5, True, False, False)
pcom_0108 = Course('PCOM 0108', 'Tech Development 2', 18, 2, True, False, False)

# term 3 PCOM core courses
pcom_0202 = Course('PCOM 0202', 'Advance Business Presentation', 33, 1.5, True, False, False)
pcom_0103 = Course('PCOM 0103', 'Canadian Workplace Culture', 35, 1.5, True, False, False)
pcom_0109_module_1 = Course('PCOM 0109 Module 1', 'Resume and Cover Letter', 8, 2, True, False, False)
pcom_0109_module_2 = Course('PCOM 0109 Module 2', 'Interview Practice', 6, 2, True, False, False)

# term 1 BCOM core courses
pcom_0203 = Course('PCOM 0203', 'Effective Professional Writing', 15, 1.5, True, False, False)
supr_0751 = Course('SUPR 0751', 'Fundamentals of Management and Supervision', 7, 2, True, False, False)
pcom_0204 = Course('PCOM 0204', 'Business Persuasion and Research', 35, 1.5, True, False, False)
supr_0837 = Course('SUPR 0837', 'Building an Engaged Workforce', 7, 2, True, False, False)
supr_0841 = Course('SUPR 0841', 'Change Management Fundamentals', 7, 2, True, False, False)
cmsk_0237 = Course('CMSK 0237', 'Google Suite Essentials', 12, 1.5, True, True, False)

# term 2 BCOM core courses
supr_0821 = Course('SUPR_0821', 'Foundations of Leadership 1', 7, 2, True, False, False)
supr_0822 = Course('SUPR_0822', 'Foundations of Leadership 1', 7, 2, True, False, False)
supr_0718 = Course('SUPR_0718', 'Effective Professional Writing', 7, 2, True, False, False)
supr_0836 = Course('SUPR_0836', 'Effective Professional Writing', 7, 2, True, False, False) 
pcom_0106 = Course('PCOM_0106', 'Effective Professional Writing', 34, 2, True, False, False)
avdm_0199 = Course('AVDM_0199', 'Effective Professional Writing', 3, 1.5, True, True, False)  

# term 3 BCOM core courses
pcom_0205 = Course('PCOM_0205', 'Small Business and Entrpreneurship in Canada', 30, 3, True, False, False)
pcom_TBD  = Course('PCOM_TBD',  'Story Telling (Public Speaking)', 21, 1.5, True, False, False)
pcom_0207 = Course('PCOM_0207', 'Developing Your Emotional Intelligence', 6, 2, True, False, False)
supr_0863 = Course('SUPR_0863', 'Design Thinking', 7, 2, True, False, False)
pcom_0206 = Course('PCOM_0206', 'Fundamentals of Agile Methodology', 6, 3, True, False, False)
#avdm_0260 = Course('PAVDM_0260', 'WordPress for Web Page Publishing', 6, 1.5, True, True, False)

pcom_courses = {
    'term 1': [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235],
    'term 2': [pcom_0102, pcom_0201, pcom_0108],
    'term 3': [pcom_0202, pcom_0103, pcom_0109_module_1, pcom_0109_module_2],
}

bcom_courses = {
    'term 1': [pcom_0203, supr_0751, pcom_0204, supr_0837, supr_0841, cmsk_0237],
    'term 2': [supr_0821, supr_0822, supr_0718, supr_0836, pcom_0106, avdm_0199],
    'term 3': [pcom_0205, pcom_TBD , pcom_0207, supr_0863, pcom_0206],
}

# Program Courses------------------------------------------------------------------
# term 1 PM program courses
prdv_0201 = Course("PRDV 0201", "NA", 21, 2, False, False, False)
prdv_0202 = Course("PRDV 0202", "NA", 14, 2, False, False, False)
prdv_0203 = Course("PRDV 0203", "NA", 21, 2, False, False, False)

# term 2 PM program courses
prdv_0204 = Course("PRDV 0204", "NA", 14, 2, False, False, False)
prdv_0205 = Course("PRDV 0205", "NA", 21, 2, False, False, False)
pcom_0130 = Course("PCOM 0130", "NA", 21, 2, False, False, False) #TODO: Schedule pcom_0130 halfway through term
prdv_0206 = Course("PRDV 0206", "NA", 14, 2, False, False, False)

# term 3 PM program courses
prdv_0207 = Course("PRDV 0207", "NA", 14, 2, False, False, False)
pcom_0131 = Course("PCOM 0131", "NA", 39, 2, False, False, False)

# term 1 BA program courses
prdv_0640 = Course("PRDV 0640", "NA", 21, 2, False, False, False)
prdv_0652 = Course("PRDV 0652", "NA", 14, 2, False, False, False)
prdv_0653 = Course("PRDV 0653", "NA", 21, 2, False, False, False)
prdv_0642 = Course("PRDV 0642", "NA", 14, 2, False, False, False)

# term 2 BA program courses
prdv_0644 = Course("PRDV 0644", "NA", 21, 2, False, False, False)
prdv_0648 = Course("PRDV 0648", "NA", 14, 2, False, False, False)
pcom_0140 = Course("PCOM 0140", "NA", 35, 2, False, False, False) #TODO: Schedule pcom_0130 halfway through term

# term 3 BA program courses
prdv_0646 = Course("PRDV 0646", "NA", 14, 2, False, False, False)
pcom_0141 = Course("PCOM 0141", "NA", 39, 3, False, False, False)

# term 1 BK program courses
acct_0201 = Course("ACCT 0201", "NA", 18, 2, False, False, False)
acct_0202 = Course("ACCT 0202", "NA", 12, 2, False, False, False)
acct_0203 = Course("ACCT 0203", "NA", 12, 2, False, False, False)

# term 2 BK program courses
acct_0206 = Course("ACCT 0206", "NA", 12, 2, False, False, False)
acct_0210 = Course("ACCT 0210", "NA", 28, 2, False, False, True )
acct_0211 = Course("ACCT 0211", "NA", 28, 2, False, False, True)

# term 3 BK program courses
acct_0208 = Course("ACCT 0208", "NA", 21, 2, False, False, True )
acct_9901 = Course("ACCT 9901", "NA", 33, 2, False, False, True )

pm_courses = {
    'term 1': [prdv_0201, prdv_0202, prdv_0203],
    'term 2': [prdv_0204, prdv_0205, pcom_0130, prdv_0206],
    'term 3': [prdv_0207, pcom_0131],
}

ba_courses = {
    'term 1': [prdv_0640, prdv_0652, prdv_0653, prdv_0642],
    'term 2': [prdv_0644, prdv_0648, pcom_0140],
    'term 3': [prdv_0646, pcom_0141],
}

bkc_courses = {
    'term 1': [acct_0201, acct_0202, acct_0203],
    'term 2': [acct_0206, acct_0210, acct_0211],
    'term 3': [acct_0208, acct_9901],
}

lab_courses = [pcom_0107, cmsk_0233, cmsk_0235, pcom_0108, pcom_0109_module_1]

term_courses = {
    # fall semester has term 1 and term 3 courses
    1: pcom_courses['term 1'] + bcom_courses['term 1'] + pcom_courses['term 3'] + bcom_courses['term 3'],
    # winter semester has term 1 and 2 courses
    2: pcom_courses['term 1'] + bcom_courses['term 1'] + pcom_courses['term 2'] + bcom_courses['term 2'],
    # spring/summer semester has term 2 and 3 courses
    3: pcom_courses['term 2'] + bcom_courses['term 2'] + pcom_courses['term 3'] + bcom_courses['term 3'], 
}

program_lab_courses = [acct_0210, acct_0211, acct_0208, acct_9901]

program_term_courses = {
    # fall semester has term 1 and term 3 courses
    1: pm_courses['term 1'] + pm_courses['term 3'] + ba_courses['term 1'] + ba_courses['term 3'] + bkc_courses['term 1'] + bkc_courses['term 3'],
    # winter semester has term 1 and 2 courses
    2: pm_courses['term 1'] + pm_courses['term 2'] + ba_courses['term 1'] + ba_courses['term 2'] + bkc_courses['term 1'] + bkc_courses['term 2'],
    # spring/summer semester has term 2 and 3 courses
    3: pm_courses['term 2'] + pm_courses['term 3'] + ba_courses['term 2'] + ba_courses['term 3'] + bkc_courses['term 2'] + bkc_courses['term 3'], 
}

room_533 = Classroom('11-533', 36, False)
room_534 = Classroom('11-534', 36, False)
room_560 = Classroom('11-560', 24, False)
room_562 = Classroom('11-562', 24, False)
room_564 = Classroom('11-564', 24, False)
room_458 = Classroom('11-458', 40, False)
room_430 = Classroom('11-430', 30, False)
room_320 = Classroom('11-320', 30, False)
room_532 = Classroom('11-532', 30, True )

lecture_rooms = [room_533, room_534, room_560, room_562, room_564, room_458, room_430, room_320]
lab_rooms = [room_532]

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

