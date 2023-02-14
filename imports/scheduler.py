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
course_rooms = {
    '11-533': ['PCOM 0101', 'PCOM 0105', 'PCOM 0107'],
    '11-534': ['PCOM 0101', 'PCOM 0105', 'PCOM 0202'],
    '11-560': ['PCOM 0105', 'PCOM 0107', 'CMSK 0233'],
    '11-562': ['CMSK 0233', 'CMSK 0235', 'PCOM 0103'],
    '11-564': ['PCOM 0102', 'PCOM 0201', 'PCOM 0108'],
    '11-458': ['PCOM 0102', 'PCOM 0108', 'PCOM 0109'],
    '11-430': ['PCOM 0102', 'PCOM 0201', 'PCOM 0108'],
    '11-320': ['PCOM 0202', 'PCOM 0103', 'PCOM 0109']
    
}

# 8 AM - 4:30 PM in half-hour increments
times = [datetime.time(i, j).strftime("%H:%M") for i in range (8, 18) for j in [0, 30]]
times.append(datetime.time(5, 0).strftime("%H:%M"))
# ==============================================================================
def make_schedule_df():
    '''
    Create empty pandas dataframes to represent the monday and wednesday 
    schedules for all rooms
    '''
    global mon_schedule, wed_schedule

    mon_schedule = pd.DataFrame(index = times)
    wed_schedule = pd.DataFrame(index = times)
    
    for room in course_rooms.keys():
        mon_schedule[room] = [""] * 21
        wed_schedule[room] = [""] * 21
    
    return

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

def find_opening(room_sched, blocks):
    '''
    Helper function for checking if a room is available for a specific time period
    on a given day. Returns the starting index (time) of when the room becomes
    available. If no availability is found, returns -1
    '''
    
    # number of time blocks required to fit lecture into schedule
    opening = [""] * blocks
    # iterators for sliding window
    left  = 0
    right = blocks
    
    while (right < len(room_sched) + 1):    
        if room_sched[left:right] == opening:
            return left
        left  += 1
        right += 1
    
    return False

def schedule_lectures(room, course, blocks):
    
    # get the column index of the current room
    room_col_index  = mon_schedule.columns.get_loc(room)
    
    # create list of row values for monday and wednesday schedules
    monday_times    = ((mon_schedule.iloc[:, [room_col_index]]))[room].tolist()
    wednesday_times = ((wed_schedule.iloc[:, [room_col_index]]))[room].tolist()
    
    # find first available time opening on monday or wednesday   
    mon_start = find_opening(monday_times, blocks)
    wed_start = find_opening(wednesday_times, blocks)
    
    if blocks <= 6 and mon_start >= 0:
        lecture = [course] * blocks
        mon_schedule.iloc[mon_start:(mon_start+blocks), room_col_index] = lecture
        return
    
    elif blocks <= 6 and wed_start >= 0:
        lecture = [course] * (blocks)
        wed_schedule.iloc[wed_start:(wed_start+blocks), room_col_index] = lecture
        return
    
    # if the lecture is too long or the room is fully booked, split the lecture into 2
    else:
        print("!!!")
    
    return

def schedule_rooms(course_rooms, weekly_hours):
    '''
    Add each room's lectures to the schedule by passing its courses, and their 
    weekly hours to the `schedule_lectures` function 
    '''
    for room in course_rooms.keys():
        for course in course_rooms[room]:
            # number of half-hour time blocks that a lecture will take up
            blocks = int(weekly_hours[course] * 2)
            schedule_lectures(room, course, blocks)

    return

if __name__ == '__main__':
    make_schedule_df()
    hours = get_weekly_hours(course_list)
    print(hours)
    
    schedule_rooms(course_rooms, hours)
    print(mon_schedule)
    print(wed_schedule)
    
    #TODO: 
    #   - make schedules local instead of global
    #   - after creating schedule, make sure any given student (PCOM or BCOM) will be able to take combination of courses
    #   - add BCOM courses & alternate scheduling between PCOM and BCOM
    #   - account for labs
    #   - check for other constraints (gap between online & in person, specific time slot reqs, etc.)
    
 