import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from itertools import chain
from typing import *
from imports.schedulers.scheduling_functions import *
from imports.classes.classrooms import *
from imports.fillClassrooms import *
from imports.classes.courses import *

def get_term_data(term: int):
    if (term == 1):
        termA = 1
        termB = 3
        start_day = getFallStartDay(2023)
        holidays = getHolidaysTuesThurs(2023)
    elif (term == 2):
        termA = 1
        termB = 2
        start_day = getWinterStartDay(2024)
        holidays = getHolidaysTuesThurs(2023)
    elif (term == 3):
        termA = 2
        termB = 3
        start_day = getSpringStartDay(2024)
        holidays = getHolidaysTuesThurs(2023)
    
    cohorts = get_cohort_counts(term)

    pmA_courses  = get_courses('PM' , termA) if cohorts[f'PM{termA}']  else []
    pmB_courses  = get_courses('PM' , termB) if cohorts[f'PM{termB}']  else []
    baA_courses  = get_courses('BA' , termA) if cohorts[f'BA{termA}']  else []
    baB_courses  = get_courses('BA' , termB) if cohorts[f'BA{termB}']  else []
    glmA_courses = get_courses('GLM', termA) if cohorts[f'GLM{termA}'] else []
    glmB_courses = get_courses('GLM', termB) if cohorts[f'GLM{termB}'] else []
    dxdA_courses = get_courses('DXD', termA) if cohorts[f'DXD{termA}'] else []
    dxdB_courses = get_courses('DXD', termB) if cohorts[f'DXD{termB}'] else []
    bkA_courses  = get_courses('BK' , termA) if cohorts[f'BK{termA}']  else []
    bkB_courses  = get_courses('BK' , termB) if cohorts[f'BK{termB}']  else []
    fsA_courses  = get_courses('FS' , termA) if cohorts[f'FS{termA}']  else []
    fsB_courses  = get_courses('FS' , termB) if cohorts[f'FS{termB}']  else []
    
    lecs = {
        'pmA' : [c for c in pmA_courses  if not c.hasLab and not c.isOnline],
        'pmB' : [c for c in pmB_courses  if not c.hasLab and not c.isOnline],
        'baA' : [c for c in baA_courses  if not c.hasLab and not c.isOnline],
        'baB' : [c for c in baB_courses  if not c.hasLab and not c.isOnline],
        'glmA': [c for c in glmA_courses if not c.hasLab and not c.isOnline],
        'glmB': [c for c in glmB_courses if not c.hasLab and not c.isOnline],
        'dxdA': [c for c in dxdA_courses if not c.hasLab and not c.isOnline],
        'dxdB': [c for c in dxdB_courses if not c.hasLab and not c.isOnline],
        'bkA' : [c for c in bkA_courses  if not c.hasLab and not c.isOnline],
        'bkB' : [c for c in bkB_courses  if not c.hasLab and not c.isOnline],
        'fsA' : [c for c in fsA_courses  if not c.hasLab and not c.isOnline],
        'fsB' : [c for c in fsB_courses  if not c.hasLab and not c.isOnline],
    }
    labs = {
        'pmA' : [c for c in pmA_courses  if c.hasLab],
        'pmB' : [c for c in pmB_courses  if c.hasLab],
        'baA' : [c for c in baA_courses  if c.hasLab],
        'baB' : [c for c in baB_courses  if c.hasLab],
        'glmA': [c for c in glmA_courses if c.hasLab],
        'glmB': [c for c in glmB_courses if c.hasLab],
        'dxdA': [c for c in dxdA_courses if c.hasLab],
        'dxdB': [c for c in dxdB_courses if c.hasLab],
        'bkA' : [c for c in bkA_courses  if c.hasLab],
        'bkB' : [c for c in bkB_courses  if c.hasLab],
        'fsA' : [c for c in fsA_courses  if c.hasLab],
        'fsB' : [c for c in fsB_courses  if c.hasLab],
    }
    online = {
        'pmA' : [c for c in pmA_courses  if c.isOnline],
        'pmB' : [c for c in pmB_courses  if c.isOnline],
        'baA' : [c for c in baA_courses  if c.isOnline],
        'baB' : [c for c in baB_courses  if c.isOnline],
        'glmA': [c for c in glmA_courses if c.isOnline],
        'glmB': [c for c in glmB_courses if c.isOnline],
        'dxdA': [c for c in dxdA_courses if c.isOnline],
        'dxdB': [c for c in dxdB_courses if c.isOnline],
        'bkA' : [c for c in bkA_courses  if c.isOnline],
        'bkB' : [c for c in bkB_courses  if c.isOnline],
        'fsA' : [c for c in fsA_courses  if c.isOnline],
        'fsB' : [c for c in fsB_courses  if c.isOnline],
    }

    course_hours = get_course_hours(list(
        chain(*list(lecs.values())+list(labs.values())+list(online.values()))
    ))
    
    # assume an absolute max of 9 cohorts (this we never be reached in practice)
    all_cohort_IDs = [f'0{i}' for i in range(1, 10)]
    
    cohorts = {
        'pmA' : all_cohort_IDs[:cohorts[f'PM{termA}']],
        'pmB' : all_cohort_IDs[:cohorts[f'PM{termB}']],
        'baA' : all_cohort_IDs[:cohorts[f'BA{termA}']],
        'baB' : all_cohort_IDs[:cohorts[f'BA{termB}']],
        'glmA': all_cohort_IDs[:cohorts[f'GLM{termA}']],
        'glmB': all_cohort_IDs[:cohorts[f'GLM{termB}']],
        'dxdA': all_cohort_IDs[:cohorts[f'DXD{termA}']],
        'dxdB': all_cohort_IDs[:cohorts[f'DXD{termB}']],
        'bkA' : all_cohort_IDs[:cohorts[f'BK{termA}']],
        'bkB' : all_cohort_IDs[:cohorts[f'BK{termB}']],
        'fsA' : all_cohort_IDs[:cohorts[f'FS{termA}']],
        'fsB' : all_cohort_IDs[:cohorts[f'FS{termB}']],
    }
    all_cohorts = [f"PM0{termA}{c}"  for c in cohorts['pmA']]  + \
                  [f"PM0{termB}{c}"  for c in cohorts['pmB']]  + \
                  [f"BA0{termA}{c}"  for c in cohorts['baA']]  + \
                  [f"BA0{termB}{c}"  for c in cohorts['baB']]  + \
                  [f"GLM0{termA}{c}" for c in cohorts['glmA']] + \
                  [f"GLM0{termB}{c}" for c in cohorts['glmB']] + \
                  [f"DXD0{termA}{c}" for c in cohorts['dxdA']] + \
                  [f"DXD0{termB}{c}" for c in cohorts['dxdB']] + \
                  [f"BK0{termA}{c}"  for c in cohorts['bkA']]  + \
                  [f"BK0{termB}{c}"  for c in cohorts['bkB']]  + \
                  [f"FS0{termB}{c}"  for c in cohorts['fsA']]  + \
                  [f"FS0{termA}{c}"  for c in cohorts['fsB']]
                  
    return { 
        'lectures': lecs,
        'labs': labs,
        'online': online,
        'course hours': course_hours,
        'start day': start_day,
        'holidays': holidays,
        'cohorts': cohorts,
        'full cohort list': all_cohorts,
    }
    

def get_sched(term: int, export=True, debug=False):
    '''
    Main driver function for generating the program course term schedule, where
    term indicates if the schedule is for fall, winter, or spring semester
    '''
    # in theory this will never happen, but just to be safe:
    if term not in [1, 2, 3]:
        return None
    
    term_data = get_term_data(term)

    c_hours  = term_data.pop("course hours")
    start    = term_data.pop("start day")
    holidays = term_data.pop("holidays")
    rooms    = get_rooms()
    
    all_cohorts = term_data.pop("full cohort list")
    
    # keep track of the current date, current day/week number, and holidays
    curr_day  = start
    date_ints = {'day': 0, 'week': 1, 'holidays': []}

    # dict mapping course titles to the day (int, not date) on which they end
    end_days = {}
    
    # starting monday dates for each week (all terms start on a wednesday)
    week_starts = [curr_day - dt.timedelta(days=2)]
    
    # create schedules for the first day, then reference this when making 
    # subsequent schedules to get consistent times and rooms for courses
    prev_scheds = make_empty_scheds(rooms)
    sched_dict = {}
    
    while curr_day < (start + dt.timedelta(weeks=13)):
        
        if curr_day not in holidays:
            new_sched = make_prgm_day_sched(term_data, c_hours, 
                                            date_ints, prev_scheds)
            
            c_hours     = update_course_hours(c_hours, new_sched)
            prev_scheds = update_schedule(c_hours, new_sched, date_ints, end_days)
            
        else:
            new_sched = pd.DataFrame({str(curr_day): ['HOLIDAY']})

        sched_dict[str(curr_day)] = new_sched
        
        if debug: print(f"\n\n{str(curr_day)}:\n{new_sched}")
        
        if (curr_day.weekday() == 0):
            curr_day += dt.timedelta(days=2)
            
        elif (curr_day.weekday() == 2):
            curr_day += dt.timedelta(days=5)
            date_ints['week'] += 1
            week_starts.append(curr_day)
            
        date_ints['day'] += 1
        
    if export:
        export_to_excel(sched_dict)
    
    return {
        "cohorts": all_cohorts,
        "week starts": week_starts,
        "last days": end_days,
        "holidays": date_ints['holidays'],
    }


if __name__ == '__main__':

    #print("Enter a number for the term you want to generate a core schedule for: \
    #      \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    get_sched(term)
