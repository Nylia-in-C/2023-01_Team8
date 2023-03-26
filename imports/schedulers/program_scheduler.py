from typing import *
import database.database as database
from imports.schedulers.scheduling_functions import *
from imports.schedulers.initialize_data import *
from imports.classes.classrooms import *
from imports.fillClassrooms import *
from imports.classes.courses import *
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

#TODO: create separate file/scheduling stuff for full stack web dev


def get_sched(term: int) -> Dict[str, pd.DataFrame]:
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

    pmA_courses  = get_courses('PM' , termA)
    pmB_courses  = get_courses('PM' , termB)
    baA_courses  = get_courses('BA' , termA)
    baB_courses  = get_courses('BA' , termB)
    glmA_courses = get_courses('GLM', termA)
    glmB_courses = get_courses('GLM', termB)
    dxdA_courses = get_courses('DXD', termA)
    dxdB_courses = get_courses('DXD', termB)
    bkA_courses  = get_courses('bkA', termA)
    bkB_courses  = get_courses('bkB', termB)
    
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
    
    rooms   = get_rooms()
    cohorts = get_cohort_counts(term)

    # list of uppercase letters, length vary
    pmA_cohorts  = string.ascii_uppercase[:cohorts[f'PM{termA}']]
    pmB_cohorts  = string.ascii_uppercase[:cohorts[f'PM{termB}']]
    baA_cohorts  = string.ascii_uppercase[:cohorts[f'BA{termA}']]
    baB_cohorts  = string.ascii_uppercase[:cohorts[f'BA{termB}']]
    glmA_cohorts = string.ascii_uppercase[:cohorts[f'GLM{termA}']]
    glmB_cohorts = string.ascii_uppercase[:cohorts[f'GLM{termB}']]
    dxdA_cohorts = string.ascii_uppercase[:cohorts[f'DXD{termA}']]
    dxdB_cohorts = string.ascii_uppercase[:cohorts[f'DXD{termB}']]
    bkA_cohorts  = string.ascii_uppercase[:cohorts[f'BK{termA}']]
    bkB_cohorts  = string.ascii_uppercase[:cohorts[f'BK{termB}']]

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
    }

    # get all 26 day schedules as a dictionary of dataframes
    # (technically, we only need the lecture objects, but having this makes
    # scheduling & debugging 1000x easier)
    full_schedule = create_program_term_schedule(
        lectures, labs, online, cohorts, rooms, start_day, holidays
    )
    
    i = 0
    for day, sched in full_schedule.items():
        print(f"\n\t\t {day} :\n")
        print(sched)
        i += 1

    print(f"holidays: {holidays}")

    return


if __name__ == '__main__':

    print("Enter a number for the term you want to generate a core schedule for: \
          \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    get_sched(term)
