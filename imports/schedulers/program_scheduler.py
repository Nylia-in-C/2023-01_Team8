import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from typing import *
from imports.schedulers.scheduling_functions import *
from imports.classes.classrooms import *
from imports.fillClassrooms import *
from imports.classes.courses import *


def get_sched(term: int, debug=False):
    '''
    Main driver function for generating the term schedule for program-specific courses, 
    where the term passed indicates if the schedule is for fall, winter, or spring semester
    '''
    # in theory this will never happen, but just to be safe:
    if term not in [1, 2, 3]:
        return None

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
        
    rooms   = get_rooms()
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
    
    pmA_lecs  = [c for c in pmA_courses  if not c.hasLab and not c.isOnline]
    pmB_lecs  = [c for c in pmB_courses  if not c.hasLab and not c.isOnline]
    baA_lecs  = [c for c in baA_courses  if not c.hasLab and not c.isOnline]
    baB_lecs  = [c for c in baB_courses  if not c.hasLab and not c.isOnline]
    glmA_lecs = [c for c in glmA_courses if not c.hasLab and not c.isOnline]
    glmB_lecs = [c for c in glmB_courses if not c.hasLab and not c.isOnline]
    dxdA_lecs = [c for c in dxdA_courses if not c.hasLab and not c.isOnline]
    dxdB_lecs = [c for c in dxdB_courses if not c.hasLab and not c.isOnline]
    bkA_lecs  = [c for c in bkA_courses  if not c.hasLab and not c.isOnline]
    bkB_lecs  = [c for c in bkB_courses  if not c.hasLab and not c.isOnline]
    fsA_lecs  = [c for c in fsA_courses  if not c.hasLab and not c.isOnline]
    fsB_lecs  = [c for c in fsB_courses  if not c.hasLab and not c.isOnline]
    
    pmA_labs  = [c for c in pmA_courses  if c.hasLab]
    pmB_labs  = [c for c in pmB_courses  if c.hasLab]
    baA_labs  = [c for c in baA_courses  if c.hasLab]
    baB_labs  = [c for c in baB_courses  if c.hasLab]
    glmA_labs = [c for c in glmA_courses if c.hasLab]
    glmB_labs = [c for c in glmB_courses if c.hasLab]
    dxdA_labs = [c for c in dxdA_courses if c.hasLab]
    dxdB_labs = [c for c in dxdB_courses if c.hasLab]
    bkA_labs  = [c for c in bkA_courses  if c.hasLab]
    bkB_labs  = [c for c in bkB_courses  if c.hasLab]
    fsA_labs  = [c for c in fsA_courses  if c.hasLab]
    fsB_labs  = [c for c in fsB_courses  if c.hasLab]
    
    pmA_onls  = [c for c in pmA_courses  if c.isOnline]
    pmB_onls  = [c for c in pmB_courses  if c.isOnline]
    baA_onls  = [c for c in baA_courses  if c.isOnline]
    baB_onls  = [c for c in baB_courses  if c.isOnline]
    glmA_onls = [c for c in glmA_courses if c.isOnline]
    glmB_onls = [c for c in glmB_courses if c.isOnline]
    dxdA_onls = [c for c in dxdA_courses if c.isOnline]
    dxdB_onls = [c for c in dxdB_courses if c.isOnline]
    bkA_onls  = [c for c in bkA_courses  if c.isOnline]
    bkB_onls  = [c for c in bkB_courses  if c.isOnline]
    fsA_onls  = [c for c in fsA_courses  if c.isOnline]
    fsB_onls  = [c for c in fsB_courses  if c.isOnline]

    # assume an absolute max of 9 cohorts (this we never be reached in practice)
    all_cohort_IDs = [f'0{i}' for i in range(1, 10)]
    
    pmA_cohorts  = all_cohort_IDs[:cohorts[f'PM{termA}']]
    pmB_cohorts  = all_cohort_IDs[:cohorts[f'PM{termB}']]
    baA_cohorts  = all_cohort_IDs[:cohorts[f'BA{termA}']]
    baB_cohorts  = all_cohort_IDs[:cohorts[f'BA{termB}']]
    glmA_cohorts = all_cohort_IDs[:cohorts[f'GLM{termA}']]
    glmB_cohorts = all_cohort_IDs[:cohorts[f'GLM{termB}']]
    dxdA_cohorts = all_cohort_IDs[:cohorts[f'DXD{termA}']]
    dxdB_cohorts = all_cohort_IDs[:cohorts[f'DXD{termB}']]
    bkA_cohorts  = all_cohort_IDs[:cohorts[f'BK{termA}']]
    bkB_cohorts  = all_cohort_IDs[:cohorts[f'BK{termB}']]
    fsA_cohorts  = all_cohort_IDs[:cohorts[f'FS{termA}']]
    fsB_cohorts  = all_cohort_IDs[:cohorts[f'FS{termB}']]

    lectures = {
        'pmA' : pmA_lecs,
        'pmB' : pmB_lecs,
        'baA' : baA_lecs,
        'baB' : baB_lecs,
        'glmA': glmA_lecs,
        'glmB': glmB_lecs,
        'dxdA': dxdA_lecs,
        'dxdB': dxdB_lecs,
        'bkA' : bkA_lecs,
        'bkB' : bkB_lecs,
        'fsA' : fsA_lecs,
        'fsB' : fsB_lecs,
    }
    labs = {
        'pmA' : pmA_labs,
        'pmB' : pmB_labs,
        'baA' : baA_labs,
        'baB' : baB_labs,
        'glmA': glmA_labs,
        'glmB': glmB_labs,
        'dxdA': dxdA_labs,
        'dxdB': dxdB_labs,
        'bkA' : bkA_labs,
        'bkB' : bkB_labs,
        'fsA' : fsA_labs,
        'fsB' : fsB_labs,
    }
    online = {
        'pmA' : pmA_onls,
        'pmB' : pmB_onls,
        'baA' : baA_onls,
        'baB' : baB_onls,
        'glmA': glmA_onls,
        'glmB': glmB_onls,
        'dxdA': dxdA_onls,
        'dxdB': dxdB_onls,
        'bkA' : bkA_onls,
        'bkB' : bkB_onls,
        'fsA' : fsA_onls,
        'fsB' : fsB_onls,
    }
    cohorts = {
        'pmA' : pmA_cohorts,
        'pmB' : pmB_cohorts,
        'baA' : baA_cohorts,
        'baB' : baB_cohorts,
        'glmA': glmA_cohorts,
        'glmB': glmB_cohorts,
        'dxdA': dxdA_cohorts,
        'dxdB': dxdB_cohorts,
        'bkA' : bkA_cohorts,
        'bkB' : bkB_cohorts,
        'fsA' : fsA_cohorts,
        'fsB' : fsB_cohorts,
    }

    # get all 26 day schedules as a dictionary of dataframes
    # (technically, we only need the lecture objects, but having this makes
    # scheduling & debugging 1000x easier)
    full_schedule, week_starts = create_prgm_term_schedule(
        lectures, labs, online, cohorts, rooms, start_day, holidays
    )
    
    if debug:
        for day, sched in full_schedule.items():
            print(f"\n\t\t {day} :\n")
            print(sched)
        print(f"week start dates {week_starts}")
        print(f"holidays: {holidays}")

    return week_starts


if __name__ == '__main__':

    print("Enter a number for the term you want to generate a core schedule for: \
          \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    get_sched(term)
