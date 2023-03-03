import math
import datetime
import pprint
import pandas as pd
from imports.classes.courses import *


# Dummy Data ===================================================================

# term 1 PCOM core courses (specific values are not accurate to specs)
pcom_0101 = Course('PCOM 0101', 'Business Writing 1', 35, 0, True, False, False)
pcom_0105 = Course('PCOM 0105', 'Intercultural Communication Skills', 35, 0, True, False, False)
pcom_0107 = Course('PCOM 0107', 'Tech Development 1', 18, 0, True, False, False)
cmsk_0233 = Course('CMSK 0233', 'MS Project Essentials', 7, 0, True, False, False)
cmsk_0235 = Course('CMSK 0235', 'MS Visio Essentials', 6, 0, True, False, False)

# term 2 PCOM core courses (specific values are not accurate to specs)
pcom_0102 = Course('PCOM 0102', 'Business Writing 2', 35, 0, True, False, False)
pcom_0201 = Course('PCOM 0201', 'Fundamentals of Public Speaking', 35, 0, True, False, False)
pcom_0108 = Course('PCOM 0108', 'Tech Development 2', 18, 0, True, False, False)

# term 3 PCOM core courses (specific values are not accurate to specs)
pcom_0202 = Course('PCOM 0202', 'Advance Business Presentation', 33, 0, True, False, False)
pcom_0103 = Course('PCOM 0103', 'Canadian Workplace Culture', 35, 0, True, False, False)
pcom_0109 = Course('PCOM 0109', 'The Job Hunt in Canada', 14, 0, True, False, False)

term_courses = {
    1: [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235],
    2: [pcom_0102, pcom_0201, pcom_0108],
    3: [pcom_0202, pcom_0103, pcom_0109], 
}

course_list = [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235, pcom_0102, 
               pcom_0201, pcom_0108, pcom_0202, pcom_0103, pcom_0109]

room_list = ['11-533', '11-534', '11-560', '11-562', '11-564', '11-458', 
             '11-430', '11-320']


# assuming ~70-90 new PCOM students/term requires 3 different lecture groups for each course
LECTURE_GROUPS= 3

# ==============================================================================

def create_empty_schedule():
    '''
    This function creates an empty pandas dataframe to represent the schedule 
    for a single day. The column headers are room numbers and the row indexes 
    are times (half hour increments)
    '''
    
    # 8 AM - 5 PM in half-hour increments 
    times = [datetime.time(i, j).strftime("%H:%M") for i in range (8, 18) for j in [0, 30]]
    times.append(datetime.time(5, 0).strftime("%H:%M"))
    
    sched = pd.DataFrame(index = times)
    
    for room in room_list:
        sched[room] = [""] * 21
        
    return sched
    

def get_course_hours():
    '''
    Create a dictionary that will be used to keep track of how many lecture hours
    a given course has, and how many hours it has left
    '''
    hours = {}
    for course in course_list:
        hours[course.ID] = {
            'required' : course.termHours, 
            'remaining': course.termHours,
            'scheduled': 0, 
        }
    return hours

def update_course_hours(course_hours, sched):
    '''
    Uses the latest schedule to update the remaining lecture hours for each course
    '''
    # get number of hours for each course on the schedule
    for room in room_list:
        courses = sched[room].tolist()
        for course in set(courses): # use a set to prevent repeating courses
            if (course == ""):
                continue
            
            # account for multiple lecture groups for each course
            scheduled_time = (courses.count(course) // LECTURE_GROUPS ) * 0.5
            course_hours[course]['scheduled'] += scheduled_time
            course_hours[course]['remaining'] -= scheduled_time

    return course_hours

def create_day_schedule(course_hours):
    '''
    This function takes an empty dataframe representing the schedule for a given day,
    and adds 3 lecture groups for each course, starting with the ones that have 
    the most lecture hours. To prevent scheduling conflicts, each course is limited to 1 room only
    '''
    
    sched = create_empty_schedule()

    # list of course IDs ordered by required lecture hours (descending order)
    courses = [course.ID for course in 
               sorted(course_list, key = lambda x: x.termHours, reverse = True)]
    
    # ignore courses that have been fully scheduled
    for course, hours in course_hours.items():
        if hours['remaining'] <= 0:
            courses.remove(course)
    
    for index, room in enumerate(room_list):
        # if there are more rooms that courses left, leave extra rooms empty
        if (index >= len(courses)):
            break
        
        room_col_index = sched.columns.get_loc(room)
        course = courses[index]
        
        if (course_hours[course]['remaining'] >= 1):
            blocks = 3 * LECTURE_GROUPS
        elif (course_hours[course]['remaining'] > 0.5):
            blocks = 2 * LECTURE_GROUPS
        else:
            blocks = 1 * LECTURE_GROUPS
         
        sched.iloc[:blocks, room_col_index] = ( [course] * blocks )
    
    return sched

def create_term_schedule(course_hours):
    
    full_schedule = []

    for i in range(26):
        curr_day = create_day_schedule(course_hours)
        if (i % 2 == 0):
            print(f"\n\t\t\tMONDAY (day {i+1})")
        else:
            print(f"\n\t\t\tWEDNESDAY (day {i+1})")
        print(curr_day)
        course_hours = update_course_hours(course_hours, curr_day)
        print("\n\n")
        pprint.pprint(course_hours)
        full_schedule.append(curr_day)        

    
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
    
    # KENNETH: see lines 119, 129, https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    
    course_hours = get_course_hours()
    schedule = create_term_schedule(course_hours)

    
    
    #TODO: 
    #   - account for new schedule changes
    #   - after creating schedule, make sure no students (in either program) will have a scheduling conflict (try to use LP so this isnt super slow)
    #   - account for labs
    #   - check for other constraints (gap between online & in person, specific time slot reqs, etc.)
    
 