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

bcom_1_lecs = sorted(bcom_courses['term 1'], key=lambda x: x.termHours, reverse=True)
pcom_1_lecs = sorted(pcom_lectures['term 1'], key = lambda x: x.termHours, reverse = True)
pcom_1_labs = sorted(pcom_labs['term 1'], key=lambda x: x.termHours, reverse=True)

bcom_2_lecs = sorted(bcom_courses['term 2'], key=lambda x: x.termHours, reverse=True)
pcom_2_lecs = sorted(pcom_lectures['term 2'], key=lambda x: x.termHours, reverse=True)
pcom_2_labs = sorted(pcom_labs['term 2'], key=lambda x: x.termHours, reverse=True)

bcom_3_lecs = sorted(bcom_courses['term 3'], key=lambda x: x.termHours, reverse=True)
pcom_3_lecs = sorted(pcom_lectures['term 3'], key=lambda x: x.termHours, reverse=True)
pcom_3_labs = sorted(pcom_labs['term 3'], key=lambda x: x.termHours, reverse=True)

if __name__ == '__main__':

    print("Enter a number for the term you want to generate a core schedule for: \
          \n1. Fall \n2. Winter \n3. Spring/Summer")
    term = int(input())

    if (term == 1):
        full_schedule = create_core_term_schedule(
            pcom_1_lecs, pcom_3_lecs,
            bcom_1_lecs, bcom_3_lecs, lecture_rooms
        )
    elif (term == 2):
        full_schedule = create_core_term_schedule(
            pcom_1_lecs, pcom_2_lecs,
            bcom_1_lecs, bcom_2_lecs, lecture_rooms
        )
    elif (term == 3):
        full_schedule = create_core_term_schedule(
            pcom_2_lecs, pcom_3_lecs,
            bcom_2_lecs, bcom_3_lecs, lecture_rooms
        )

    
    for day, sched in full_schedule.items():
        if not (isinstance(sched, str)):
            print(f"\n\n{day}: \n {sched}")

    # sort pcom & bcom courses in descending order of termHours, then combine the
    # lists, alternating between terms (this will prevent scheduling conflicts)
    

    # print("Enter a number for the Core Courses Schedule or the Program Schedule: \
    #       \n1. Core \n2. Program")
    # CoreOrProgram = int(input())
    
    # if CoreOrProgram == 1:
    #     print("==========================Monday Wednesday==========================")

    #     # schedule lectures & labs seperately
    #     lectures = [course for course in term_courses[term] if course not in lab_courses]
    #     labs     = [course for course in term_courses[term] if course in lab_courses]
        
    #     lecture_hours, lab_hours = get_course_hours(lectures, labs)
        
    #     full_schedule = create_term_schedule(lecture_hours, lectures, lecture_rooms, lab_hours, labs, lab_rooms)

        
    #     for day, sched in full_schedule.items():
    #         if not (isinstance(sched, str)):
    #             print(f"\n\n{day}: \n {sched}")
    
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

