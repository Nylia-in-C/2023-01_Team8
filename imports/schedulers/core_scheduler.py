import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)



from imports.classes.courses import *
from imports.fillClassrooms import *
from imports.classes.classrooms import *
from imports.schedulers.scheduling_functions import *
from itertools import chain
from typing import *

def get_term_data(term: int):
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
        
    cohorts = get_cohort_counts(term)
    
    pcomA_courses = get_courses('PCOM', termA) if cohorts[f'PCOM{termA}'] else []
    pcomB_courses = get_courses('PCOM', termB) if cohorts[f'PCOM{termB}'] else []
    bcomA_courses = get_courses('BCOM', termA) if cohorts[f'BCOM{termA}'] else []
    bcomB_courses = get_courses('BCOM', termB) if cohorts[f'BCOM{termB}'] else []
    
    lecs = {
        'pcomA': [c for c in pcomA_courses if not c.hasLab and not c.isOnline],
        'pcomB': [c for c in pcomB_courses if not c.hasLab and not c.isOnline],
        'bcomA': [c for c in bcomA_courses if not c.hasLab and not c.isOnline],
        'bcomB': [c for c in bcomB_courses if not c.hasLab and not c.isOnline],
    }
    labs = {
        'pcomA': [c for c in pcomA_courses if c.hasLab],
        'pcomB': [c for c in pcomB_courses if c.hasLab],
        'bcomA': [c for c in bcomA_courses if c.hasLab],
        'bcomB': [c for c in bcomA_courses if c.hasLab],
    }
    online = {
        'pcomA': [c for c in pcomA_courses if c.isOnline],
        'pcomB': [c for c in pcomB_courses if c.isOnline],
        'bcomA': [c for c in bcomA_courses if c.isOnline],
        'bcomB': [c for c in bcomB_courses if c.isOnline],
    }
    
    course_hours = get_course_hours(list(
        chain(*list(lecs.values())+list(labs.values())+list(online.values()))
    ))
    
    # assume an absolute max of 9 cohorts (this we never be reached in practice)
    all_cohort_IDs = [f'0{i}' for i in range(1, 10)]
    
    cohorts = {
        'pcomA': all_cohort_IDs[:cohorts[f'PCOM{termA}']],
        'pcomB': all_cohort_IDs[:cohorts[f'PCOM{termB}']],
        'bcomA': all_cohort_IDs[:cohorts[f'BCOM{termA}']],
        'bcomB': all_cohort_IDs[:cohorts[f'BCOM{termB}']],
    }
    
    all_cohorts = [f"PCOM0{termA}{c}" for c in cohorts['pcomA']] + \
                  [f"PCOM0{termB}{c}" for c in cohorts['pcomB']] + \
                  [f"BCOM0{termA}{c}" for c in cohorts['bcomA']] + \
                  [f"BCOM0{termB}{c}" for c in cohorts['bcomB']]
    
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


def get_sched(term: int, export=True, debug=False) -> Dict[str, pd.DataFrame]:
    '''
    Main driver function for generating the core course term schedule, where
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
            new_sched = make_core_day_sched(term_data, c_hours, 
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