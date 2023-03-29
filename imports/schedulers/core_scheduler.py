import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from imports.classes.courses import *
from imports.fillClassrooms import *
from imports.classes.classrooms import *
from imports.schedulers.scheduling_functions import *
from typing import *


def get_sched(term: int, debug=False) -> Dict[str, pd.DataFrame]:
    '''
    Main driver function for generating the core course term schedule, where
    term indicates if the schedule is for fall, winter, or spring semester
    '''
    # in theory this will never happen, but just to be safe:
    if term not in [1, 2, 3]:
        return None

    if (term == 1):
        termA = 1
        termB = 3
        start_day = getFallStartDay(2023)
        holidays  = getHolidaysMonWed(2023)
    elif (term == 2):
        termA = 1
        termB = 2
        start_day = getWinterStartDay(2024)
        holidays  = getHolidaysMonWed(2023)
    elif (term == 3):
        termA = 2
        termB = 3
        start_day = getSpringStartDay(2024)
        holidays  = getHolidaysMonWed(2023)
        
    rooms   = get_rooms()
    cohorts = get_cohort_counts(term)
        
    pcomA_courses = get_courses('PCOM', termA) if cohorts[f'PCOM{termA}'] else []
    pcomB_courses = get_courses('PCOM', termB) if cohorts[f'PCOM{termB}'] else []
    bcomA_courses = get_courses('BCOM', termA) if cohorts[f'BCOM{termA}'] else []
    bcomB_courses = get_courses('BCOM', termB) if cohorts[f'BCOM{termB}'] else []

    pcomA_lecs = [c for c in pcomA_courses if not c.hasLab and not c.isOnline]
    pcomB_lecs = [c for c in pcomB_courses if not c.hasLab and not c.isOnline]
    bcomA_lecs = [c for c in bcomA_courses if not c.hasLab and not c.isOnline]
    bcomB_lecs = [c for c in bcomB_courses if not c.hasLab and not c.isOnline]
    
    pcomA_labs = [c for c in pcomA_courses if c.hasLab]
    pcomB_labs = [c for c in pcomB_courses if c.hasLab]
    bcomA_labs = [c for c in bcomA_courses if c.hasLab]
    bcomB_labs = [c for c in bcomA_courses if c.hasLab]
    
    pcomA_onls = [c for c in pcomA_courses if c.isOnline]
    pcomB_onls = [c for c in pcomB_courses if c.isOnline]
    bcomA_onls = [c for c in bcomA_courses if c.isOnline]
    bcomB_onls = [c for c in bcomB_courses if c.isOnline]
    
    # assume an absolute max of 9 cohorts (this we never be reached in practice)
    all_cohort_IDs = [f'0{i}' for i in range(1, 10)]
    
    pcomA_cohorts = all_cohort_IDs[:cohorts[f'PCOM{termA}']]
    pcomB_cohorts = all_cohort_IDs[:cohorts[f'PCOM{termB}']]
    bcomA_cohorts = all_cohort_IDs[:cohorts[f'BCOM{termA}']]
    bcomB_cohorts = all_cohort_IDs[:cohorts[f'BCOM{termB}']]
    
    all_cohorts = [f"PCOM0{termA}{c}" for c in pcomA_cohorts] + \
                  [f"PCOM0{termB}{c}" for c in pcomB_cohorts] + \
                  [f"BCOM0{termA}{c}" for c in bcomA_cohorts] + \
                  [f"BCOM0{termB}{c}" for c in bcomB_cohorts]
    
    lectures = {
        'pcomA': pcomA_lecs,
        'pcomB': pcomB_lecs,
        'bcomA': bcomA_lecs,
        'bcomB': bcomB_lecs,
    }
    labs = {
        'pcomA': pcomA_labs,
        'pcomB': pcomB_labs,
        'bcomA': bcomA_labs,
        'bcomB': bcomB_labs,
    }
    online = {
        'pcomA': pcomA_onls,
        'pcomB': pcomB_onls,
        'bcomA': bcomA_onls,
        'bcomB': bcomB_onls,
    }
    cohorts = {
        'pcomA': pcomA_cohorts,
        'pcomB': pcomB_cohorts,
        'bcomA': bcomA_cohorts,
        'bcomB': bcomB_cohorts,
    }

    # get all 26 day schedules as a dictionary of dataframes
    # (technically, we only need the lecture objects, but having this makes 
    # scheduling & debugging 1000x easier)
    full_schedule, week_starts = create_core_term_schedule(
        lectures, labs, online, cohorts, rooms, start_day, holidays
    )
    
    if debug:
        for day, sched in full_schedule.items():
            print(f"\n\t\t {day} :\n")
            print(sched)
        print(f"week start dates: {week_starts}")
        print(f"holidays: {holidays}")

    return {
        "cohorts": all_cohorts,
        "week starts": week_starts 
    }


if __name__ == '__main__':

    #print("Enter a number for the term you want to generate a core schedule for: \
    #      \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    get_sched(term)