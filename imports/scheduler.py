import math
import datetime
import pprint
import pandas as pd
from classes.courses import *


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

course_list = [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235, pcom_0102, 
               pcom_0201, pcom_0108, pcom_0202, pcom_0103, pcom_0109]

room_list = ['11-533', '11-534', '11-560', '11-562', '11-564', '11-458', 
             '11-430', '11-320']

# rooms mapped to their lectures (the same course in multiple rooms indicates a different lecture group)
# assuming there are 70-90 PCOM students/term, each course will need 2 or 3 different lecture groups
room_course_dict = {
                        # term 1 courses
    '11-533': ['PCOM 0101', 'PCOM 0105', 'PCOM 0107', 'CMSK 0233', 'CMSK 0235'],
    '11-534': ['PCOM 0101', 'PCOM 0105', 'PCOM 0107', 'CMSK 0233', 'CMSK 0235'],
    '11-560': ['PCOM 0101', 'PCOM 0105', 'PCOM 0107', 'CMSK 0233', 'CMSK 0235'],
    
                        # term 2 courses
    '11-562': ['PCOM 0102', 'PCOM 0201', 'PCOM 0108'],
    '11-564': ['PCOM 0102', 'PCOM 0201', 'PCOM 0108'],
    '11-458': ['PCOM 0102', 'PCOM 0201', 'PCOM 0108'],

                        # term 3 courses
    '11-430': ['PCOM 0202', 'PCOM 0103', 'PCOM 0109'],
    '11-320': ['PCOM 0202', 'PCOM 0103', 'PCOM 0109']
    
}

# ==============================================================================
# generator for alternating between monday & wednesday schedules
def alternate_schedules(mon, wed):
    while True:
        yield mon
        yield wed

def create_intital_schedule():
    '''
    This function creates 2 empty pandas dataframes to represent the 
    monday and wednesday schedules. The column headers are room numbers 
    and the row indexes are times (half hour increments)
    '''
    
    # 8 AM - 5 PM in half-hour increments 
    times = [datetime.time(i, j).strftime("%H:%M") for i in range (8, 18) for j in [0, 30]]
    times.append(datetime.time(5, 0).strftime("%H:%M"))
    
    sched = pd.DataFrame(index = times)
    
    for room in room_list:
        sched[room]    = [""] * 21
        
    return sched

def get_course_hours():
    '''
    Create a dictionary that maps courses to information on how many lecture hours 
    it requires and hwo many it already has
    '''
    hours = {}
    for course in course_list:
        hours[course.ID] = {
            'required' : course.termHours, 
            'remaining': course.termHours,
            'scheduled': 0, 
        }
    return hours

def get_reschedule_day(course_hours):
    '''
    This function takes a dictionary of courses mapped to their lecture hour
    information, finds the courses that are currently being scheduled
    and returns the number of days until the schedule will need updating
    (i.e. a currently scheduled course reaches its lecture hours requirement)
    '''
    # lowest number of lecture hours remaining for courses being scheduled
    curr_min = float('inf')
    for hours in course_hours.values():
        if (hours['required'] <= hours['scheduled']):
            continue
        curr_min = min(curr_min, hours['remaining'])
        
    # return the number of days needed to reach `curr_min` lecture hours
    return math.ceil(curr_min / 1.5)

def update_course_hours(course_hours, sched):
    '''
    This function uses the schedule for a single day (monday or wednesday) to 
    update the of scheduled and remaining hour counts in course_hours
    '''
    # get number of hours for each course on the schedule
    for room in room_list:
        courses = sched[room].tolist()
        for course in courses:
            if (course == ""):
                continue
            course_hours[course]['scheduled'] += 0.5
            course_hours[course]['remaining'] -= 0.5

    return course_hours

def create_day_schedule(sched, course_hours, blocks):
    '''
    This function takes an empty dataframe representing the schedule for a given day,
    and adds 3 lecture groups for each course, starting with the ones that have 
    the most lecture hours. To prevent scheduling conflicts, each course is limited to 1 room only
    '''

    # list of course IDs ordered by required lecture hours (descending order)
    courses = [course.ID for course in 
               sorted(course_list, key = lambda x: x.termHours, reverse = True)]
    
    # ignore courses that have been fully scheduled
    for course, hours in course_hours.items():
        if hours['remaining'] <= 0:
            courses.remove(course)
    
    for index, room in enumerate(room_list):
        room_col_index = sched.columns.get_loc(room)
        sched.iloc[:blocks, room_col_index] = ( [courses[index]] * blocks)
    
    return sched

def create_term_schedule():
    course_hours = get_course_hours()
    
    # number of days until schedule needs to be changed
    days_until_update = get_reschedule_day(course_hours)
    print(f"\ndays until rescheduling: {days_until_update}\n")
    
    week = 1
    
    for i in range(days_until_update):
        sched = create_intital_schedule()
        create_day_schedule(sched, course_hours, 6)
        course_hours = update_course_hours(course_hours, sched)
        
        if (i % 2 == 0):
            print(f"\t\t\tMONDAY WEEK {week}: \n")
        else:
            print(f"\t\t\tWEDNESDAY WEEK {week}: \n")
            week += 1
    
        print(sched)

    return


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
    
    create_term_schedule()
    
    
    #TODO: 
    #   - after creating schedule, make sure no students (in either program) will have a scheduling conflict (try to use LP so this isnt super slow)
    #   - account for labs
    #   - check for other constraints (gap between online & in person, specific time slot reqs, etc.)
    
 