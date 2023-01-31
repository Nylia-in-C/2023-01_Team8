# module for creating cohort objects from parsed file data
# for right now, we're assuming that the number of students in each program is passed 
# as a dictionary. eg: {'PM': 17, 'BA': 20, 'GLM': 14, 'FS': 19, 'DXD': 18, 'BK': 18}
# Term IDs are hardcoded for now, and will need to change once we implement file upload/parsing

import random
from itertools import cycle
from imports.classes.cohorts import Cohort

# constants (testing only)
CLASSROOMS = [36, 36, 24, 24, 24, 40, 30, 30, 30]
TERM_ID    = "01"

def random_students():
    '''
    Randomly generates a dictionary mapping programIDs to their student counts (testing purposes only)
    '''
    programs = ["PM", "BA", "GLM", "FS", "DXD", "BK"]
    counts = {}
    total = 0
    while total < 90 or total > 120:
        for i in range(6):
            num = random.randint(4,20)
            counts[programs[i]] = num
            total = sum(counts.values())
    return counts

def get_optimal_cohort_size(program_count, class_sizes):
    '''
    returns the optimal cohort size based on how many classroom seats are left 
    unused, and how well the number of students in a given program divide 
    into cohorts of that size
    '''
    cohorts = []
    for cohort_size in range(4, min(program_count.values()) + 1):
        # total number of unused class seats for a given cohort size
        CR_sum = sum([(class_size % cohort_size ) for class_size in class_sizes])
        # total number of extra students not in a cohort
        SR_sum = sum([min((count % cohort_size), cohort_size-(count % cohort_size)) 
                      for count in program_count.values()])
        
        # add total remainders for each cohort size to list (necessary for sorting)
        cohorts.append((cohort_size, (CR_sum + SR_sum)))
        
    # sort cohorts from lowest to highest remainders
    cohorts.sort(key=lambda x: x[1])
    
    return cohorts[0][0]

def partition_students(student_count, cohort_size):
    '''
    Divides the number of students (dividend) by chosen cohort size (divisor),
    returning a list representing the number of students in each cohort 
    '''
    cohorts = []
    while student_count >= cohort_size:
        quotient, remainder = divmod(student_count, cohort_size)
        cohorts.extend([cohort_size] * quotient)
        student_count = remainder
        
    # finished creating cohorts, need to deal w remainder now
    if student_count > (cohort_size // 2):   # student remainder is close enough to cohort size
        cohorts.append(student_count)         
    else:                               
        groups = cycle(cohorts)
        for group in groups:                 # add remaining students to a cohort one-by-one
            if student_count == 0:
                break
            group += 1
            student_count -= 1
            next(groups)
    
    return cohorts


def create_cohort_dict(students, cohort_size):
    '''
    Calls the `partition_students` function to create cohort sizes for each 
    program. Returns a dictionary mapping programIDs to integer lists
    '''
    result = {}
    for program, count in students.items():
        result[program] = partition_students(count, cohort_size)
    return result

def make_cohorts():
#===testing purposes only=======================================================
    program_count = random_students()
    print(f"program counts: {program_count}\n")

    optimal_size = get_optimal_cohort_size(program_count, CLASSROOMS)
    print(f"optimal cohort size: {optimal_size}")
    
    cohort_dict = create_cohort_dict(program_count, optimal_size)
    print(f"cohort: {cohort_dict}\n\n")
    
    #TODO: make cohort objects directly, instead of dictionaries first (maybe)
    
    results = []   
    for program in cohort_dict.keys():
        for cohort_size in cohort_dict[program]:
            new_cohort = Cohort(program, TERM_ID, cohort_size)
            results.append(new_cohort)
    
    for cohort in results:
        print(cohort)
    
    
#===============================================================================
    
if __name__ == '__main__':
    make_cohorts()