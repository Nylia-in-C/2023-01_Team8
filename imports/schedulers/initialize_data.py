import os, sys
from imports.classes.courses import *
from imports.classes.classrooms import *
from typing import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

# term 1 PCOM courses
pcom_0101 = Course('PCOM 0101', 'Business Writing 1', 35,1, 1.5, True, False, False)
pcom_0105 = Course('PCOM 0105', 'Intercultural Communication Skills', 35,1, 1.5, True, False, False)
pcom_0107 = Course('PCOM 0107', 'Tech Development 1', 18,1, 2, True, False, True)
cmsk_0233 = Course('CMSK 0233', 'MS Project Essentials', 7, 1, 2, True, False, True)
cmsk_0235 = Course('CMSK 0235', 'MS Visio Essentials', 6, 1, 2, True, False, True)

# term 2 PCOM core courses
pcom_0102 = Course('PCOM 0102', 'Business Writing 2', 35,2, 1.5, True, False, False)
pcom_0201 = Course('PCOM 0201', 'Fundamentals of Public Speaking', 35,2, 1.5, True, False, False)
pcom_0108 = Course('PCOM 0108', 'Tech Development 2', 18, 2, 2, True, False, True)

# term 3 PCOM core courses
pcom_0202 = Course('PCOM 0202', 'Advance Business Presentation', 33,3, 1.5, True, False, False)
pcom_0103 = Course('PCOM 0103', 'Canadian Workplace Culture', 35,3, 1.5, True, False, False)
pcom_0109_module_1 = Course('PCOM 0109 M1', 'Resume and Cover Letter', 8, 3, 2, True, False, True)
pcom_0109_module_2 = Course('PCOM 0109 M2', 'Interview Practice', 6,3, 2, True, False, False)

# term 1 BCOM core courses
pcom_0203 = Course('PCOM 0203', 'Effective Professional Writing', 15,1,  1.5, True, False, False)
supr_0751 = Course('SUPR 0751', 'Fundamentals of Management and Supervision', 7,1, 2, True, False, False)
pcom_0204 = Course('PCOM 0204', 'Business Persuasion and Research', 35,1, 1.5, True, False, False)
supr_0837 = Course('SUPR 0837', 'Building an Engaged Workforce', 7,1, 2, True, False, False)
supr_0841 = Course('SUPR 0841', 'Change Management Fundamentals', 7,1, 2, True, False, False)
cmsk_0237 = Course('CMSK 0237', 'Google Suite Essentials', 12,1, 1.5, True, True, False)

# term 2 BCOM core courses
supr_0821 = Course('SUPR_0821', 'Foundations of Leadership 1', 7,2, 2, True, False, False)
supr_0822 = Course('SUPR_0822', 'Foundations of Leadership 1', 7,2, 2, True, False, False)
supr_0718 = Course('SUPR_0718', 'Effective Professional Writing', 7,2, 2, True, False, False)
supr_0836 = Course('SUPR_0836', 'Effective Professional Writing', 7,2, 2, True, False, False) 
pcom_0106 = Course('PCOM_0106', 'Effective Professional Writing', 34,2, 2, True, False, False)
avdm_0199 = Course('AVDM_0199', 'Effective Professional Writing', 3,2, 1.5, True, True, False)  

# term 3 BCOM core courses
pcom_0205 = Course('PCOM_0205', 'Small Business and Entrpreneurship in Canada', 30,3, 3, True, False, False)
pcom_TBD  = Course('PCOM_TBD',  'Story Telling (Public Speaking)', 21,3, 1.5, True, False, False)
pcom_0207 = Course('PCOM_0207', 'Developing Your Emotional Intelligence', 6,3, 2, True, False, False)
supr_0863 = Course('SUPR_0863', 'Design Thinking', 7,3, 2, True, False, False)
pcom_0206 = Course('PCOM_0206', 'Fundamentals of Agile Methodology', 6,3, 3, True, False, False)
avdm_0260 = Course('AVDM_0260', 'WordPress for Web Page Publishing', 6,3, 1.5, True, True, False)

pcom_courses = [pcom_0101, pcom_0105, pcom_0107, cmsk_0233, cmsk_0235, pcom_0102, 
                pcom_0201, pcom_0108, pcom_0202, pcom_0103, pcom_0109_module_1, 
                pcom_0109_module_2, ]

bcom_courses = [pcom_0203, supr_0751, pcom_0204, supr_0837, supr_0841, cmsk_0237, 
                supr_0821, supr_0822, supr_0718, supr_0836, pcom_0106, avdm_0199, 
                pcom_0205, pcom_TBD, pcom_0207, supr_0863, pcom_0206, avdm_0260]


# Program Courses------------------------------------------------------------------
# term 1 PM program courses
prdv_0201 = Course("PRDV 0201", "NA", 21,1, 2, False, False, False)
prdv_0202 = Course("PRDV 0202", "NA", 14,1, 2, False, False, False)
prdv_0203 = Course("PRDV 0203", "NA", 21,1, 2, False, False, False)

# term 2 PM program courses
prdv_0204 = Course("PRDV 0204", "NA", 14,2, 2, False, False, False)
prdv_0205 = Course("PRDV 0205", "NA", 21,2, 2, False, False, False)
pcom_0130 = Course("PCOM 0130", "NA", 21,2, 2, False, False, False) 
prdv_0206 = Course("PRDV 0206", "NA", 14,2, 2, False, False, False)

# term 3 PM program courses
prdv_0207 = Course("PRDV 0207", "NA", 14,3, 2, False, False, False)
pcom_0131 = Course("PCOM 0131", "NA", 39,3, 2, False, False, False)

# term 1 BA program courses
prdv_0640 = Course("PRDV 0640", "NA", 21,1, 2, False, False, False)
prdv_0652 = Course("PRDV 0652", "NA", 14,1, 2, False, False, False)
prdv_0653 = Course("PRDV 0653", "NA", 21,1, 2, False, False, False)
prdv_0642 = Course("PRDV 0642", "NA", 14,1, 2, False, False, False)

# term 2 BA program courses
prdv_0644 = Course("PRDV 0644", "NA", 21,2, 2, False, False, False)
prdv_0648 = Course("PRDV 0648", "NA", 14,2, 2, False, False, False)
pcom_0140 = Course("PCOM 0140", "NA", 35,2, 2, False, False, False) 

# term 3 BA program courses
prdv_0646 = Course("PRDV 0646", "NA", 14,3, 2, False, False, False)
pcom_0141 = Course("PCOM 0141", "NA", 39,3, 3, False, False, False)

# term 1 BK program courses
acct_0201 = Course("ACCT 0201", "NA", 18,1, 2, False, False, False)
acct_0202 = Course("ACCT 0202", "NA", 12,1, 2, False, False, False)
acct_0203 = Course("ACCT 0203", "NA", 12,1, 2, False, False, False)

# term 2 BK program courses
acct_0206 = Course("ACCT 0206", "NA", 12,2, 2, False, False, False)
acct_0210 = Course("ACCT 0210", "NA", 28,2, 2, False, False, True )
acct_0211 = Course("ACCT 0211", "NA", 28,2, 2, False, False, True)

# term 3 BK program courses
acct_0208 = Course("ACCT 0208", "NA", 21,3, 2, False, False, True )
acct_9901 = Course("ACCT 9901", "NA", 33,3, 2, False, False, True )


pm_courses = {
    'term 1': [prdv_0201, prdv_0202, prdv_0203],
    'term 2': [prdv_0204, prdv_0205, pcom_0130, prdv_0206],
    'term 3': [prdv_0207, pcom_0131],
}

ba_courses = {
    'term 1': [prdv_0640, prdv_0652, prdv_0653, prdv_0642],
    'term 2': [prdv_0644, prdv_0648, pcom_0140],
    'term 3': [prdv_0646, pcom_0141],
}

bkc_courses = {
    'term 1': [acct_0201, acct_0202, acct_0203],
    'term 2': [acct_0206, acct_0210, acct_0211],
    'term 3': [acct_0208, acct_9901],
}

# lab_courses = [pcom_0107, cmsk_0233, cmsk_0235, pcom_0108, pcom_0109_module_1]

# term_courses = {
#     # fall semester has term 1 and term 3 courses
#     1: pcom_courses['term 1'] + bcom_courses['term 1'] + pcom_courses['term 3'] + bcom_courses['term 3'],
#     # winter semester has term 1 and 2 courses
#     2: pcom_courses['term 1'] + bcom_courses['term 1'] + pcom_courses['term 2'] + bcom_courses['term 2'],
#     # spring/summer semester has term 2 and 3 courses
#     3: pcom_courses['term 2'] + bcom_courses['term 2'] + pcom_courses['term 3'] + bcom_courses['term 3'], 
# }

program_lab_courses = [acct_0210, acct_0211, acct_0208, acct_9901]

program_term_courses = {
    # fall semester has term 1 and term 3 courses
    1: pm_courses['term 1'] + pm_courses['term 3'] + ba_courses['term 1'] + ba_courses['term 3'] + bkc_courses['term 1'] + bkc_courses['term 3'],
    # winter semester has term 1 and 2 courses
    2: pm_courses['term 1'] + pm_courses['term 2'] + ba_courses['term 1'] + ba_courses['term 2'] + bkc_courses['term 1'] + bkc_courses['term 2'],
    # spring/summer semester has term 2 and 3 courses
    3: pm_courses['term 2'] + pm_courses['term 3'] + ba_courses['term 2'] + ba_courses['term 3'] + bkc_courses['term 2'] + bkc_courses['term 3'], 
}

room_533 = Classroom('11-533', 36, False)
room_534 = Classroom('11-534', 36, False)
room_560 = Classroom('11-560', 24, False)
room_562 = Classroom('11-562', 24, False)
room_564 = Classroom('11-564', 24, False)
room_458 = Classroom('11-458', 40, False)
room_430 = Classroom('11-430', 30, False)
room_320 = Classroom('11-320', 30, False)
room_532 = Classroom('11-532 (LAB)', 30, True )
online   = Classroom('ONLINE', 1000, False)      # need this for scheduling functions to work properly

rooms = [room_533, room_534, room_560, room_562, room_564, 
         room_458, room_430, room_320, room_532, online]