import math
import datetime
import pandas as pd
from classes.courses import *


# Dummy Data ===================================================================

# term 1 PCOM core courses (specific values are not accurate to specs)
pcom_0101 = Course('PCOM 0101', 'Business Writing 1', 35, 0, True, False, False)
pcom_0105 = Course('PCOM 0105', 'Intercultural Communication Skills', 35, 0, True, False, False)
pcom_0107 = Course('PCOM 0107', 'Tech Development 1', 35, 0, True, False, False)
cmsk_0233 = Course('CMSK 0233', 'MS Project Essentials', 21, 0, True, False, False)
cmsk_0235 = Course('CMSK 0235', 'MS Visio Essentials', 18, 0, True, False, False)

course_list = [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235]

# rooms mapped to their lectures (repeated courses indicate a different lecture group)
course_rooms = {
    '11-533': ['PCOM 0101', 'PCOM 0101', 'CMSK 0233', 'CMSK 0233'],
    '11-534': ['PCOM 0101', 'PCOM 0101', 'PCOM 0105', 'PCOM 0105'],
    '11-458': ['PCOM 0107'],
    '11-430': ['PCOM 0107', 'CMSK 0235', 'CMSK 0235']
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
    # TODO: 
    # get rid of global variables, figure out a less greasy way of handling teh schedule
    global mon_schedule, wed_schedule

    mon_schedule = pd.DataFrame(index = times)
    wed_schedule = pd.DataFrame(index = times)
    
    for room in course_rooms.keys():
        mon_schedule[room] = [""] * 21
        wed_schedule[room] = [""] * 21
    
    # format schedules
    # wed_schedule = wed_schedule.reset_index()
    # mon_schedule = mon_schedule.reset_index()
    
    # print("\n\t\tMONDAY SCHEDULE:\n")
    # print(mon_schedule)
    # print("\n\t\tWEDNESDAY SCHEDULE:\n")
    # print(wed_schedule)
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
    available. If no availability is found, returns False
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
    
    if blocks <= 6 and mon_start != False:
        # schedule lecture for monday
        lecture = [course] * blocks
        mon_schedule.iloc[mon_start:(mon_start+blocks), room_col_index] = lecture
        return
    
    elif blocks <= 6 and wed_start != False:
        lecture = [course] * (blocks)
        wed_schedule.iloc[wed_start:(wed_start+blocks), room_col_index] = lecture
        pass
    
    # if the lecture is too long or the room is fully booked, split the lecture into 2
    else:
        pass
    
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
    
    # room = '11-533'
    # course = 'TEST'
    # blocks = 6
    
    # room_col_index  = mon_schedule.columns.get_loc(room)
    # monday_times    = (mon_schedule.iloc[:, [room_col_index]])
    
    # for i in range(10):
    #     monday_times.iloc[[i], [0]] = 'abc'
    
    # mon_start = find_opening((monday_times[room]).tolist(), blocks)

    # lecture = [course] * (blocks)
    # mon_schedule.iloc[mon_start:(mon_start+blocks), room_col_index] = lecture
    # print(mon_schedule)
    
 