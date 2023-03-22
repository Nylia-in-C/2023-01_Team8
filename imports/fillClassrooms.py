#===================================================================================================
# Imports
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import random
from classes.classrooms import *
from classes.legions    import *
from classes.courses    import *
from classes.programs   import *
from create_legions     import *
from database.database  import *

#===================================================================================================
# Setup
COREHOURS       = 2*13*9
PROGRAMHOURS    = 2*13*8.5 #days*weeks*hours
FSPRROGRAMHOURS = 2*13*4
#PROGRAMHOURS = 60
#COREHOURS

programCoursesByTerm = {}

rooms = []

ghostRooms = []

roomHours = {
    "Core": {},
    "Program": {},
    "FS": {} 
}


#===================================================================================================
# Functions
def delete_ghost_rooms():
    connection = create_connection(r".\database\database.db")

    deleteClassroomItem(connection, 'ghost%')

    close_connection(connection)
    
def add_ghost_room(hasLab):
    """
    Adds ghost room to ghostRooms global variable
    """
    connection = create_connection(r".\database\database.db")
    database_ghosts = readClassroomItem(connection, 'ghost%')
    close_connection(connection)

    ghostID = f"ghost-{len(ghostRooms) + len(database_ghosts) + 1}"
    ghostRoom = Classroom(ghostID, 30, hasLab)

    rooms.append(ghostRoom)
    ghostRooms.append(ghostRoom)
    roomHours["Core"][ghostID]    = 0
    roomHours["Program"][ghostID] = 0
    roomHours["FS"][ghostID]      = 0

def enough_hours(program, cohorts, isCore):
    """
    If there are not enough hours left to support every cohort in a program, make a new ghostroom and return True
    Else return False
    """
    # Uses a copy of the hours for each room
    temp_roomHours = roomHours[isCore].copy()

    if   isCore == "Core": maxHours = COREHOURS
    elif isCore == "FS":   maxHours = FSPRROGRAMHOURS
    else:                  maxHours = PROGRAMHOURS 

    for cohort_count in cohorts:
        for course in programCoursesByTerm[program]:
            scheduled = False

            for room in rooms:
                # Fits courses in rooms with enough hours
                if temp_roomHours[room.ID] + course.termHours <= maxHours and room.isLab == course.hasLab:
                    temp_roomHours[room.ID] += course.termHours
                    scheduled = True
                    break

            #No room had enough hours to accomadate a course     
            if not scheduled:
                add_ghost_room(course.hasLab) 
                return False
    return True

def cohorts_fits(program, cohorts, isCore):
    """
    If there is enough time and space to accomadate all cohorts in a program, save it in roomHours and return True
    Else return false
    """
    global roomHours
    # Uses a copy of the hours for each room
    temp_roomHours = roomHours[isCore].copy()

    if   isCore == "Core": maxHours = COREHOURS
    elif isCore == "FS":   maxHours = FSPRROGRAMHOURS
    else:                  maxHours = PROGRAMHOURS 

    for cohort_count in cohorts:
        for course in programCoursesByTerm[program]:
            scheduled = False

            for room in rooms:
                # Fits courses in rooms with enough hours and capacity
                if temp_roomHours[room.ID] + course.termHours <= maxHours and room.isLab == course.hasLab and room.capacity >= cohort_count:
                    temp_roomHours[room.ID] += course.termHours
                    scheduled = True
                    break

            #No room had enough hours and capacity to accomadate a course    
            if not scheduled: return False
    
    #Update the room hours
    roomHours[isCore] = temp_roomHours.copy()
    return True

def fillPrograms(program_counts):
    """
    Takes the number of students in each program and sees if they all fit. If they don't all fit, add ghost rooms.

    Takes a dictionary of programs with the number of students in each program.

    Adds ghost rooms to database.
    """
    for program in program_counts.keys():
        if programCoursesByTerm[program][0].isCore: isCore = "Core"
        elif program[0:2] == "FS":                  isCore = "FS"
        else:                                       isCore = "Program"

        total_size = program_counts[program]
        number_of_cohorts = 1
        cohorts = [total_size]

        scheduled = False
        while not scheduled:

            # Check if remaining rooms have enough time left
            # if not, add ghost room
            if not enough_hours(program, cohorts, isCore): 
                # Try again with 1 cohort
                number_of_cohorts = 1
                cohorts = [total_size]
                continue
            
            # Check if remaining rooms have enough seat capacity
            # if not, add another cohort
            if not cohorts_fits(program, cohorts, isCore):
                number_of_cohorts += 1
                cohorts = [int(total_size)//number_of_cohorts for i in range(number_of_cohorts)]
                for i in range(total_size%number_of_cohorts):
                    cohorts[i] += 1
                
            else: 
                scheduled = True
                print(program + ':', cohorts)

def fillClassrooms(term):
    """
    Loads course and room data from database, calculates ghostrooms, and adds ghostrooms to the database.

    Need to load students from database.
    """
    global programCoursesByTerm
    global rooms
    global ghostRooms
    global roomHours

    programCoursesByTerm = {}
    rooms = []
    ghostRooms = []
    roomHours = {
        "Core": {},
        "Program": {},
        "FS": {} 
    }

    connection = create_connection(r".\database\database.db")

    #--------------------------------------------------------
    # Pull Courses from database
    if   term == 1: term = "13"
    elif term == 2: term = "21"
    elif term == 3: term = "32"

    programString = readProgramItem(connection, '%')
    for program in programString:
        course = readCourseItem(connection, program[1])
        if course == []: continue
        
        course = course[0]
        if int(course[5]) == 1: isCore = True
        else:                   isCore = False
        if int(course[6]) == 1: isOnline = True
        else:                   isOnline = False
        if int(course[7]) == 1: hasLab = True
        else:                   hasLab = False
        course = Course(course[0], course[1], int(course[2]), int(course[3]), int(course[4]), isCore, isOnline, hasLab)

        if str(course.term) not in term: continue

        programTerm = f"{program[0]}{course.term}"
        if programTerm not in programCoursesByTerm.keys(): programCoursesByTerm[programTerm] = []
        programCoursesByTerm[programTerm].append(course)

    # Random generation: Remove when getting actual inputs
    program_counts = {}
    for key in programCoursesByTerm.keys():
        program_counts[key] = random.randint(18, 189)

    #--------------------------------------------------------
    # Pull Classrooms from database
    classrooms = readClassroomItem(connection, '%')
    for room in classrooms:
        isLab = False
        if int(room[2]) == 1: isLab = True
        rooms.append(Classroom(room[0], int(room[1]), isLab))

    for room in rooms:
        roomHours["Core"][room.ID]    = 0
        roomHours["Program"][room.ID] = 0
        roomHours["FS"][room.ID]      = 0
    
    rooms.sort(key= lambda Classroom: Classroom.capacity)

    #--------------------------------------------------------
    # Calculate ghost rooms
    fillPrograms(program_counts)

    for room in ghostRooms:
        addClassroomItem(connection, room)
    
    close_connection(connection)

# TODO:
#   - Take student count input
#   - Adding ghostroom calls database for next id

# Nice to have:
#   - Reduced program hours only on lab rooms
#   - Programs with the most students are scheduled first
#   - Extensive testing: Efficient and proper fill
#   - When ghost room is added do entire scheduling again?
#   - Add rhyme and reason to ghostroom capacity in add_ghost_room()
#   - Better cohort split algorithm


#===================================================================================================
if __name__ == '__main__':
    # print(rooms, ghostRooms)
    # add_ghost_room(True)
    # print(rooms, ghostRooms)

    # print(rooms, ghostRooms)
    # print(enough_hours("PM01", [36, 24]))
    # print(rooms, ghostRooms)

    # print(rooms, ghostRooms, roomHours)
    # print(cohorts_fits("PM01", [40, 24]))
    # print(rooms, ghostRooms, roomHours)

    # add_ghost_room(False)
    # for room in ghostRooms:
    #         connection = create_connection(r".\database\database.db")
    #         addClassroomItem(connection, room)
    #         close_connection(connection)

    # program_counts = {}
    # for key in programCoursesByTerm.keys():
    #     program_counts[key] = random.randint(18, 189)
    # fillPrograms(program_counts)
    # print(roomHours)
    # print(ghostRooms)

    fillClassrooms(3)
    print(roomHours)
    print(ghostRooms)
    fillClassrooms(1)
    print(roomHours)
    print(ghostRooms)
    fillClassrooms(2)
    print(roomHours)
    print(ghostRooms)

    # delete_ghost_rooms()