# module for creating cohort objects from parsed file data
# for right now, we're assuming that the number of students in each program is passed 
# as a dictionary. eg: {'PM': 17, 'BA': 20, 'GLM': 14, 'FS': 19, 'DXD': 18, 'BK': 18}
# Term IDs are hardcoded for now, and will need to change once we implement file upload/parsing

import random

# constants
CLASSROOMS = [36, 36, 24, 24, 24, 40, 30, 30, 30,36,36]
OPTIMAL_SIZES = [6, 4, 5]       # top 3 cohort sizes ordered from best to worst

# testing only
TERM_ID    = "01"

def random_students():
    '''
    Randomly generates a dictionary mapping programIDs to their student counts (testing purposes only)
    '''
    programs = ["PM", "BA", "GLM", "FS", "DXD", "BK"]
    counts = {}
    total = 0
    while total < 100 or total > 250:
        for i in range(6):
            num = random.randint(15,40)
            counts[programs[i]] = num
            total = sum(counts.values())
    return counts

#This isnt being used, but we'll keep it on the off-chance that the classroom sizes change
def get_optimal_cohort_size(program_count, class_sizes):
    '''
    returns the optimal cohort size based on how many classroom seats are left 
    unused, and how well the number of students in a given program divide 
    into cohorts of that size.
    '''
    cohorts = []
    for cohort_size in range(6, min(program_count.values()) + 1):
        # total number of unused class seats for a given cohort size
        CR_sum = sum([(class_size % cohort_size ) for class_size in class_sizes])
        # total number of extra students not in a cohort
        SR_sum = sum([min((count % cohort_size), cohort_size-(count % cohort_size)) 
                      for count in program_count.values()])
        
        # add total remainders for each cohort size to list (necessary for sorting)
        cohorts.append((cohort_size, (CR_sum + SR_sum)))
        
    # sort cohorts from lowest to highest remainders
    cohorts.sort(key=lambda x: x[1])
    
    return cohorts

def partition_students(count):
    '''
    Takes in the number of students applying to a specific program, and returns
    a list of how the number as a linear combination of 6, 4 and 5 (in order of preference)
    This works for all integers except for 1, 2, 3, and 7 (handled as edge cases)
    '''
    if count <= 3:
        return [count]
    
    if count == 7:
        return [4, 3]
    
    for i in range((count // 5) + 1):
        for j in range((count // 4) + 1):
            k = count - (i * 5) - (j * 4)
            if k >= 0 and k % 6 == 0:       # in theory this should always be true
                return ([6] * (k // 6)) + ([4] * j) + ([5] * i)

    return None


def create_cohort_dict(students):
    '''
    Calls the `partition_students` function to create cohort sizes for each 
    program. Returns a dictionary mapping programIDs to integer lists
    '''
    result = {}
    for program, count in students.items():
        result[program] = partition_students(count)
    return result

def make_cohorts():
#===testing purposes only=======================================================
    program_count = random_students()
    print(f"program counts: {program_count}\n")
    
    res = create_cohort_dict(program_count)
    print(res)
    
    
    #TODO: make cohort objects directly, instead of dictionaries first (maybe)

    
#===============================================================================
    
if __name__ == '__main__':
    make_cohorts()