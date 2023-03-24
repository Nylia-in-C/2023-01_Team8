import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from imports.classes.courses import *
from imports.fillClassrooms import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
from imports.schedulers.scheduling_functions import *
import database.database as database
from imports.schedulers.initialize_data import *
from typing import *


def get_sched(term: int) -> Dict[str, pd.DataFrame]:
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

    pcomA_lecs = get_lectures('PCOM', termA)
    pcomB_lecs = get_lectures('PCOM', termB)
    bcomA_lecs = get_lectures('BCOM', termA)
    bcomB_lecs = get_lectures('BCOM', termB)
    
    # only pcom has labs
    pcomA_labs = get_labs('PCOM', termA)
    pcomB_labs = get_labs('PCOM', termB)
    
    # only bcom has online courses
    bcomA_onls = get_onlines('BCOM', termA)
    bcomB_onls = get_onlines('BCOM', termB)
        
    rooms   = get_rooms()
    cohorts = get_cohort_counts(term)
    
    # list of uppercase letters, length vary
    pcomA_cohorts = string.ascii_uppercase[:cohorts[f'PCOM{termA}']]
    pcomB_cohorts = string.ascii_uppercase[:cohorts[f'PCOM{termB}']]
    bcomA_cohorts = string.ascii_uppercase[:cohorts[f'BCOM{termA}']]
    bcomB_cohorts = string.ascii_uppercase[:cohorts[f'BCOM{termB}']]
    
    lectures = {
        'pcomA': pcomA_lecs,
        'pcomB': pcomB_lecs,
        'bcomA': bcomA_lecs,
        'bcomB': bcomB_lecs,
    }
    labs = {
        'pcomA': pcomA_labs,
        'pcomB': pcomB_labs,
    }
    online = {
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
    full_schedule = create_core_term_schedule(
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