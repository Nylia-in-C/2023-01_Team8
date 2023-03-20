import os, sys
from imports.classes.courses import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
from imports.schedulers.scheduling_functions import *
from typing import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

# for each term and core program, create a list of lab courses and lecture courses
# sort these lists in descending order of term hours & use them to create a dictionary
# of DataFrame schedules

pcom_1_lectures = [course for course in pcom_courses if course.term == 1 and 
                   not course.hasLab and not course.isOnline]
pcom_2_lectures = [course for course in pcom_courses if course.term == 2 and 
                   not course.hasLab and not course.isOnline]
pcom_3_lectures = [course for course in pcom_courses if course.term == 3 and 
                   not course.hasLab and not course.isOnline]

bcom_1_lectures = [course for course in bcom_courses if course.term == 1 and 
                   not course.hasLab and not course.isOnline]
bcom_2_lectures = [course for course in bcom_courses if course.term == 2 and 
                   not course.hasLab and not course.isOnline]
bcom_3_lectures = [course for course in bcom_courses if course.term == 3 and 
                   not course.hasLab and not course.isOnline]

# only pcom has labs
pcom_1_labs = [course for course in pcom_courses if course.term == 1 and course.hasLab]
pcom_2_labs = [course for course in pcom_courses if course.term == 2 and course.hasLab]
pcom_3_labs = [course for course in pcom_courses if course.term == 3 and course.hasLab]

# only bcom has online courses
bcom_1_online = [course for course in bcom_courses if course.term == 1 and course.isOnline]
bcom_2_online = [course for course in bcom_courses if course.term == 2 and course.isOnline]
bcom_3_online = [course for course in bcom_courses if course.term == 3 and course.isOnline]


def get_sched(term: int) -> Dict[str, pd.DataFrame]:
    
    # in theory this will never happen, but just to be safe:
    if term not in [1,2,3]: 
        return None
    
    if (term == 1):
        lectures = {
            'pcom': {'term A': pcom_1_lectures, 'term B': pcom_3_lectures},
            'bcom': {'term A': bcom_1_lectures, 'term B': bcom_3_lectures},
        }
        labs   = { 'pcom': {'term A': pcom_1_labs, 'term B': pcom_3_labs} }
        onls = { 'bcom': {'term A': bcom_1_online, 'term B': bcom_3_online} }

    elif (term == 2):
        lectures = {
            'pcom': {'term A': pcom_1_lectures, 'term B': pcom_2_lectures},
            'bcom': {'term A': bcom_1_lectures, 'term B': bcom_2_lectures},
        }
        labs   = { 'pcom': {'term A': pcom_1_labs, 'term B': pcom_2_labs} }
        onls = { 'bcom': {'term A': bcom_1_online, 'term B': bcom_2_online} }

    elif (term == 3):
        lectures = {
            'pcom': {'term A': pcom_2_lectures, 'term B': pcom_3_lectures},
            'bcom': {'term A': bcom_2_lectures, 'term B': bcom_3_lectures},
        }
        labs   = { 'pcom': {'term A': pcom_2_labs, 'term B': pcom_3_labs} }
        onls = { 'bcom': {'term A': bcom_2_online, 'term B': bcom_3_online} }
        
    return create_core_term_schedule(lectures, labs, onls, rooms)
        


if __name__ == '__main__':

    print("Enter a number for the term you want to generate a core schedule for: \
          \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    full_schedule = get_sched(term)

    for day, sched in full_schedule.items():
        # if (day > 5):
        #     break
        print(f"\n\t\t {day} :\n")
        print(sched)

