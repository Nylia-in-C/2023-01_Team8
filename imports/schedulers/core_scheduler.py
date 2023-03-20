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

pcom_1_lectures = [course for course in pcom_courses if course.term == 1 and not course.hasLab]
pcom_2_lectures = [course for course in pcom_courses if course.term == 2 and not course.hasLab]
pcom_3_lectures = [course for course in pcom_courses if course.term == 3 and not course.hasLab]

bcom_1_lectures = [course for course in bcom_courses if course.term == 1 and not course.hasLab]
bcom_2_lectures = [course for course in bcom_courses if course.term == 2 and not course.hasLab]
bcom_3_lectures = [course for course in bcom_courses if course.term == 3 and not course.hasLab]

pcom_1_labs = [course for course in pcom_courses if course.term == 1 and course.hasLab]
pcom_2_labs = [course for course in pcom_courses if course.term == 2 and course.hasLab]
pcom_3_labs = [course for course in pcom_courses if course.term == 3 and course.hasLab]

bcom_1_labs = [course for course in bcom_courses if course.term == 1 and course.hasLab]
bcom_2_labs = [course for course in bcom_courses if course.term == 2 and course.hasLab]
bcom_3_labs = [course for course in bcom_courses if course.term == 3 and course.hasLab]
def get_sched(term: int) -> Dict[str, pd.DataFrame]:
    
    # in theory this will never happen, but just to be safe:
    if term not in [1,2,3]: 
        return None
    
    if (term == 1):
        lectures = {
            'pcom': {'term A': pcom_1_lectures, 'term B': pcom_3_lectures},
            'bcom': {'term A': bcom_1_lectures, 'term B': bcom_3_lectures},
        }
        labs = {
            'pcom': {'term A': pcom_1_labs, 'term B': pcom_3_labs},
            'bcom': {'term A': bcom_1_labs, 'term B': bcom_3_labs},
        }

    elif (term == 2):
        lectures = {
            'pcom': {'term A': pcom_1_lectures, 'term B': pcom_2_lectures},
            'bcom': {'term A': bcom_1_lectures, 'term B': bcom_2_lectures},
        }
        labs = {
            'pcom': {'term A': pcom_1_labs, 'term B': pcom_2_labs},
            'bcom': {'term A': bcom_1_labs, 'term B': bcom_2_labs},
        }

    elif (term == 3):
        lectures = {
            'pcom': {'term A': pcom_2_lectures, 'term B': pcom_3_lectures},
            'bcom': {'term A': bcom_2_lectures, 'term B': bcom_3_lectures},
        }
        labs = {
            'pcom': {'term A': pcom_2_labs, 'term B': pcom_3_labs},
            'bcom': {'term A': bcom_2_labs, 'term B': bcom_3_labs},
        }
        
    return create_core_term_schedule(lectures, labs, rooms)
        


if __name__ == '__main__':

    print("Enter a number for the term you want to generate a core schedule for: \
          \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    full_schedule = get_sched(term)

    for day, sched in enumerate(full_schedule):
        # if (day > 5):
        #     break
        print(f"\n\t\t {day} :\n")
        print(sched)
    
    
    # if CoreOrProgram == 2:
    #     print("==========================Tuesday Thursday==========================")

    #     # Program schedule
    #     # program-lectures
    #     program_lectures = [course for course in program_term_courses[term] if course not in program_lab_courses]
    #     # program-hours
    #     program_labs     = [course for course in program_term_courses[term] if course in program_lab_courses]

    #     program_lecture_hours, program_lab_hours = get_course_hours(program_lectures, program_labs)

    #     program_full_schedule = create_term_schedule(program_lecture_hours, program_lectures, lecture_rooms, program_lab_hours, program_labs, lab_rooms)

    #     for day, sched in program_full_schedule.items():
    #         if not (isinstance(sched, str)):
    #             print(f"\n\n{day}: \n {sched}")
    
    #Notes:
    #   - Classes don't have a consistent starting time. When classes drop out of the schedule they get shifted up.
    #   - Only one course is scheduled per room per day. Most impactful for labs, lots of empty space where labs could squeeze

    #TODO: 
    #   - write function to validate no scheduling conflicts (no 'horizontal' overlap between cohorts)
    #   - initialize course & classroom objects in seperate file
    #   - create lecture objects rather than creating/displaying dataframe (maybe)

