import math
import datetime
import pprint
import pandas as pd
from classes.courses import *
from classes.classrooms import *
import string




#initialize objects/dummy data==================================================

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
pcom_0109_module_2 = Course('PCOM 0109 Module 2', 'Resume and Cover Letter', 8, 2, True, False, False)


pcom_courses = {
    'term 1': [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235],
    'term 2': [pcom_0102, pcom_0201, pcom_0108],
    'term 3': [pcom_0202, pcom_0103, pcom_0109_module_1, pcom_0109_module_2]
}

lab_courses = [pcom_0107, cmsk_0233, cmsk_0235, pcom_0108, pcom_0109_module_1]

term_courses = {
    # fall semester has term 1 and term 3 courses
    1: pcom_courses['term 1'] + pcom_courses['term 3'],
    # winter semester has term 1 and 2 courses
    2: pcom_courses['term 1'] + pcom_courses['term 2'],
    # spring/summer semester has term 2 and 3 courses
    3: pcom_courses['term 2'] + pcom_courses['term 3'], 
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

# assuming ~70-90 new PCOM students/term requires 3 different lecture groups for each course
COHORT_COUNT = 3
# ==============================================================================
def create_empty_schedule(room_tuple):
    '''
    This function creates an empty pandas dataframe to represent the schedule 
    for a single day. The column headers are room numbers and the row indexes 
    are times (half hour increments)
    '''
    room_list = list(room_tuple)
    # 8 AM - 5 PM in half-hour increments 
    times = [datetime.time(i, j).strftime("%H:%M") for i in range (8, 18) for j in [0, 30]]
    times.append(datetime.time(5, 0).strftime("%H:%M"))
    
    sched = pd.DataFrame(index = times)
    
    for room in (room_list):
        if (room.isLab):
            sched[f"{room.ID} (LAB)"] = [""] * 21
        else:
            sched[room.ID] = [""] * 21
        
    return sched
    
def get_course_hours(lectures, labs):
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

def update_course_hours(course_hours, prev_schedule):
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

def create_day_schedule(course_hours, course_list, room_list):

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
        
        # add identifiers to differentiate between cohorts
        # use built-in string library since we dont necessarily know how the number of cohorts
        cohorts = []
        for i in range(COHORT_COUNT):
            cohort_str = curr_course.ID + "-" + string.ascii_uppercase[i]
            cohorts.extend([cohort_str] * blocks)
            
        # to prevent schedule conflicts, put lectures in the morning and labs in the evening
        if room.isLab:
            sched.iloc[-(blocks*COHORT_COUNT):, room_col_index] = cohorts
        else:
            sched.iloc[:(blocks*COHORT_COUNT), room_col_index] = cohorts
    
    return sched


def create_term_schedule(lecture_hours, lectures, lecture_rooms, lab_hours, labs, lab_rooms):
    
    full_schedule = {}

    for i in range(1, 27):

        
        lecture_sched = create_day_schedule(lecture_hours, lectures, lecture_rooms)
        lecture_hours = update_course_hours(lecture_hours, lecture_sched)
        
        lab_sched = create_day_schedule(lab_hours, labs, lab_rooms)
        lab_hours = update_course_hours(lab_hours, lab_sched)
        
        full_day_sched = lecture_sched.join(lab_sched)
        
        # add place holders to `full_schedule` dict to avoid duplicates
        if any(full_day_sched.equals(day_sched) for day_sched in list(full_schedule.values())):
            full_schedule[f"day {i}"] = "-"
            
        else:
            full_schedule[f"day {i}"] = full_day_sched      

    
    return full_schedule


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
    

    # schedule lectures & labs seperately
    lectures = [course for course in term_courses[term] if course not in lab_courses]
    labs     = [course for course in term_courses[term] if course in lab_courses]
    
    lecture_hours, lab_hours = get_course_hours(lectures, labs)
    
    full_schedule = create_term_schedule(lecture_hours, lectures, lecture_rooms, lab_hours, labs, lab_rooms)

    
    for day, sched in full_schedule.items():
        if not (isinstance(sched, str)):
            print(f"\n\n{day}: \n {sched}")
            
    
    
    #TODO: 
    #   - schedule BCOM
    #   - initialize course & classroom objects in seperate file
    #   - create lecture objects rather than creating/displaying dataframe (maybe)

