import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from imports.classes.courses import *
from imports.classes.classrooms import *
from imports.schedulers.initialize_data import *
from imports.schedulers.scheduling_functions import *
import database.database as database
from typing import *




def get_program_rows(program: str) -> List[str]:
    db = r".\database\database.db"  # database.db file path
    connection = database.create_connection(db)
    
    query = f"SELECT C.* FROM Courses C JOIN Programs P ON C.CourseID = P.CourseID WHERE P.ProgID = '{program}';"
    
    try:
        cur = connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    except:
        print("unable to retrieve core courses from database")
        database.close_connection(connection)
        return None
    
    database.close_connection(connection)
    return rows

def get_program_courses(program: str) -> List[Course]:
    
    rows = get_program_rows(program)
    
    courses = []
    for row in rows:
        row = list(row)
        # convert 0/1 to booleans
        for i in range(5,8):
            if   row[i] == 0: row[i] = False
            elif row[i] == 1: row[i] = True
            
        courses.append( 
            Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) 
        )
        
    return courses

def get_term_courses(termA: int, termB: int) -> Tuple[Dict[str, Dict[str, Course]]]:
    pcom = get_program_courses("PCOM")
    bcom = get_program_courses("BCOM")

    
    pcomA_lecs = [c for c in pcom if c.term == termA and not c.hasLab and not c.isOnline]
    pcomB_lecs = [c for c in pcom if c.term == termB and not c.hasLab and not c.isOnline]
    
    bcomA_lecs = [c for c in bcom if c.term == termA and not c.hasLab and not c.isOnline]
    bcomB_lecs = [c for c in bcom if c.term == termB and not c.hasLab and not c.isOnline]
    
    pcomA_labs = [c for c in pcom if c.term == termA and c.hasLab]
    pcomB_labs = [c for c in pcom if c.term == termB and c.hasLab]
    
    bcomA_onls = [c for c in bcom if c.term == termA and c.isOnline]
    bcomB_onls = [c for c in bcom if c.term == termB and c.isOnline] 
    
    lectures = {
        'pcom': {
            'term A': pcomA_lecs, 
            'term B': pcomB_lecs
        },
        'bcom': {
            'term A': bcomA_lecs, 
            'term B': bcomB_lecs
        }
    }
    labs = {
        'pcom': {
            'term A': pcomA_labs, 
            'term B': pcomB_labs
        }
    }
    online = {
        'bcom': {
            'term A': bcomA_onls, 
            'term B': bcomB_onls
        }
    }
    
    return lectures, labs, online
    

def get_sched(term: int) -> Dict[str, pd.DataFrame]:
    
    # in theory this will never happen, but just to be safe:
    if term not in [1,2,3]: 
        return None
    
    if (term == 1):
        lectures, labs, online = get_term_courses(1, 3)

    elif (term == 2):
        lectures, labs, online = get_term_courses(1, 2)

    elif (term == 3):
        lectures, labs, online = get_term_courses(2, 3)
        
    return create_core_term_schedule(lectures, labs, online, rooms)
        

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
        
        
    
