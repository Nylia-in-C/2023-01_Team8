import math
import datetime
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

course_list = [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235,
               pcom_0102, pcom_0201, pcom_0108, pcom_0202, pcom_0103, pcom_0109]

# rooms mapped to their lectures (repeated courses indicate a different lecture group)
# assuming ~90 PCOM students/term, each course will have ~3 different lecture groups
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

# 8 AM - 5 PM in half-hour increments 
times = [datetime.time(i, j).strftime("%H:%M") for i in range (8, 18) for j in [0, 30]]
times.append(datetime.time(5, 0).strftime("%H:%M"))

# empty schedules for monday and wednesday
mon_schedule = pd.DataFrame(index = times)
wed_schedule = pd.DataFrame(index = times)
# ==============================================================================

def get_weekly_hours(course_list):
    '''
    Calculate how many lecture hours per week each course should have
    '''
    hours = {}
    for course in course_list:
        weekly_avg = course.termHours / 13
        # round up to the nearest half-hour
        weekly_hours = math.ceil(weekly_avg * 2) / 2
        hours[course.ID] = weekly_hours
     
    return hours

def get_available_time(room_sched, blocks):
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
        start  += 1
        end += 1
    
    return -1

def book_room(room, course, blocks, day):
    '''
    This function schedules a lecture in a given room. Using the existing schedule
    for a specific day and the length of the lecture, it first tries to retreive an
    available start time. If lectures are over 3 hours or no start time is found,
    it splits the lecture time in half, and schedules 2 lectures for the week.
    '''
    if (day not in ['mon', 'wed']):
        return 
    
    elif (day == 'mon'):
        room_col_index = mon_schedule.columns.get_loc(room)
        times = ((mon_schedule.iloc[:, [room_col_index]]))[room].tolist()
        
    elif (day == 'wed'):
        room_col_index = wed_schedule.columns.get_loc(room)
        times = ((wed_schedule.iloc[:, [room_col_index]]))[room].tolist()
    
    start_time = get_available_time(times, blocks)
    
    if blocks <= 6 and start_time >= 0:
        lecture = [course] * blocks
        if (day == 'mon'):
            mon_schedule.iloc[start_time:(start_time+blocks), room_col_index] = lecture
        elif (day == 'wed'):
            wed_schedule.iloc[start_time:(start_time+blocks), room_col_index] = lecture
    else:
        print("!!!")
        return
    return


def schedule_rooms(course_rooms, weekly_hours):
    '''
    Add each room's lectures to the schedule by passing its courses, and their 
    weekly hours to the `schedule_lectures` function 
    '''
    for room in course_rooms.keys():
        for index, course in enumerate(course_rooms[room]):
            
            # number of half-hour time blocks that a lecture will take up
            blocks = int(weekly_hours[course] * 2)
            
            # alternate between monday & wednesday scheduling
            if (index % 2 == 0):
                book_room(room, course, blocks, 'mon')
            else:
                book_room(room, course, blocks, 'wed')
    return

if __name__ == '__main__':
    # add empty slots to monday and wednesday schedules 
    for room in room_course_dict.keys():
        mon_schedule[room] = [""] * 21
        wed_schedule[room] = [""] * 21
    
    hours = get_weekly_hours(course_list)
    print(hours)
    
    schedule_rooms(room_course_dict, hours)
    print(mon_schedule)
    print(wed_schedule)
    
    #TODO: 
    #   - after creating schedule, make sure no students (in either program) will have a scheduling conflict
    #   - add BCOM courses & alternate scheduling between PCOM and BCOM
    #   - account for labs
    #   - check for other constraints (gap between online & in person, specific time slot reqs, etc.)
    
 