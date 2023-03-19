
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
PROGRAMHOURS    = 2*13*9 #days*weeks*hours
FSPRROGRAMHOURS = 2*13*4
#PROGRAMHOURS = 60
#COREHOURS



programCoursesByTerm = {
    "PM01":  [Course("PRDV 0201", "NA", 21, 1, 2, False, False, False), Course("PRDV 0202", "NA", 14, 1, 2, False, False, False), Course("PRDV 0203", "NA", 21, 1, 2, False, False, False)], 
    "PM02":  [Course("PRDV 0204", "NA", 14, 2, 2, False, False, False), Course("PRDV 0205", "NA", 21, 2, 2, False, False, False), Course("PCOM 0130", "NA", 21, 2, 2, False, False, False), Course("PRDV 0206", "NA", 14, 2, 2, False, False, False)], 
    "PM03":  [Course("PRDV 0207", "NA", 14, 3, 2, False, False, False), Course("PCOM 0131", "NA", 39, 3, 2, False, False, False)],
    "BA01":  [Course("PRDV 0640", "NA", 21, 1, 2, False, False, False), Course("PRDV 0652", "NA", 14, 1, 2, False, False, False), Course("PRDV 0653", "NA", 21, 1, 2, False, False, False), Course("PRDV 0642", "NA", 14, 1, 2, False, False, False)], 
    "BA02":  [Course("PRDV 0644", "NA", 21, 2, 2, False, False, False), Course("PRDV 0648", "NA", 14, 2, 2, False, False, False), Course("PCOM 0140", "NA", 35, 2, 2, False, False, False)], 
    "BA03":  [Course("PRDV 0646", "NA", 14, 3, 2, False, False, False), Course("PCOM 0141", "NA", 39, 3, 3, False, False, False)],
    "GLM01": [Course("SCMT 0501", "NA", 21, 1, 2, False, False, False), Course("SCMT 0502", "NA", 21, 1, 2, False, False, False), Course("PRDV 0304", "NA", 15, 1, 2, False, False, False)], 
    "GLM02": [Course("SCMT 0503", "NA", 15, 2, 2, False, False, False), Course("SCMT 0504", "NA", 21, 2, 2, False, False, False)],
    "GLM03": [Course("SCMT 0505", "NA", 21, 3, 2, False, False, False), Course("PCOM 0151", "NA", 39, 3, 3, False, False, False)],
    #"FS01":  [Course("CMSK 0150", "NA", 16, 1, 2, False, False, True ), Course("CMSK 0151", "NA", 16, 1, 2, False, False, True ), Course("CMSK 0152", "NA", 16, 1, 2, False, False, True ), Course("CMSK 0157", "NA", 16, 1, 2, False, False, True ), Course("CMSK 0154", "NA", 16, 1, 2, False, False, True )], 
    #"FS02":  [Course("CMSK 0153", "NA", 18, 2, 2, False, False, True ), Course("CMSK 0200", "NA", 16, 2, 2, False, False, True ), Course("CMSK 0201", "NA", 18, 2, 2, False, False, True ), Course("CMSK 0203", "NA", 16, 2, 2, False, False, True ), Course("CMSK 0202", "NA", 18, 2, 2, False, False, True )], 
    #"FS03":  [Course("PCOM 0160", "NA", 50, 3, 2, False, False, True )],
    "DXD01": [Course("AVDM 0165", "NA", 18, 1, 2, False, False, True ), Course("DXDI 0101", "NA", 24, 1, 2, False, False, True ), Course("DXDI 0102", "NA", 24, 1, 2, False, False, True )], 
    "DXD02": [Course("AVDM 0170", "NA", 18, 2, 2, False, False, True ), Course("AVDM 0138", "NA", 18, 2, 2, False, False, True ), Course("DXDI 0103", "NA", 24, 2, 2, False, False, True ), Course("DXDI 0104", "NA", 24, 2, 2, False, False, True )], 
    "DXD03": [Course("AVDM 0238", "NA", 18, 3, 2, False, False, True ), Course("AVDM 0270", "NA", 18, 3, 2, False, False, True ), Course("DXDI 9901", "NA", 45, 3, 2, False, False, True )],
    "BKC01": [Course("ACCT 0201", "NA", 18, 1, 2, False, False, False), Course("ACCT 0202", "NA", 12, 1, 2, False, False, False), Course("ACCT 0203", "NA", 12, 1, 2, False, False, False)], 
    "BKC02": [Course("ACCT 0206", "NA", 12, 2, 2, False, False, False), Course("ACCT 0210", "NA", 28, 2, 2, False, False, True ), Course("ACCT 0211", "NA", 28, 2, 2, False, False, True)], 
    "BKC03": [Course("ACCT 0208", "NA", 21, 3, 2, False, False, True ), Course("ACCT 9901", "NA", 33, 3, 2, False, False, True ) ],
    "PCOM01": [Course('PCOM 0101', 'Business Writing 1', 35,1, 1.5, True, False, False), Course('PCOM 0105', 'Intercultural Communication Skills', 35,1, 1.5, True, False, False), Course('PCOM 0107', 'Tech Development 1', 18,1, 2, True, False, True), Course('CMSK 0233', 'MS Project Essentials', 7,1, 2, True, False, True), Course('CMSK 0235', 'MS Visio Essentials', 6,1, 2, True, False, True)]
}

coreCoursesByTerm = {
    "PCOM01": [Course('PCOM 0101', 'Business Writing 1', 35,1, 1.5, True, False, False), Course('PCOM 0105', 'Intercultural Communication Skills', 35,1, 1.5, True, False, False), Course('PCOM 0107', 'Tech Development 1', 18,1, 2, True, False, True), Course('CMSK 0233', 'MS Project Essentials', 7,1, 2, True, False, True), Course('CMSK 0235', 'MS Visio Essentials', 6,1, 2, True, False, True)]
}

rooms = [
         Classroom("11-458", 40, False),
         Classroom("11-533", 36, False), 
         Classroom("11-534", 36, False),
         Classroom("11-430", 30, False), 
         Classroom("11-320", 30, False),
         Classroom("11-560", 24, False),
         Classroom("11-562", 24, False),
         Classroom("11-564", 24, False),
         Classroom("11-532", 30, True ) 
         ]
rooms.sort(key= lambda Classroom: Classroom.capacity)

ghostRooms = []

roomHours = {
    "Core": {
             "11-458": 0,
             "11-533": 0, 
             "11-534": 0,
             "11-430": 0, 
             "11-320": 0,
             "11-560": 0,
             "11-562": 0,
             "11-564": 0,
             "11-532": 0
    },
    "Program": {
             "11-458": 0,
             "11-533": 0, 
             "11-534": 0,
             "11-430": 0, 
             "11-320": 0,
             "11-560": 0,
             "11-562": 0,
             "11-564": 0,
             "11-532": 0
    } 
}

fsRoomHours = {"11-532": 0}

roomFill  = {"11-458": [],
             "11-533": [], 
             "11-534": [],
             "11-430": [], 
             "11-320": [],
             "11-560": [],
             "11-562": [],
             "11-564": [],
             "11-532": []}



#===================================================================================================
# Random Generation
def random_students_by_term():
    '''
    Randomly generates a dictionary mapping programIDs to their student counts (testing purposes only)
    '''
    programs = ["PM01",  "PM02",  "PM03",
                "BA01",  "BA02",  "BA03", 
                "GLM01", "GLM02", "GLM03", 
                "FS01",  "FS02",  "FS03", 
                "DXD01", "DXD02", "DXD03", 
                "BKC01", "BKC02", "BKC03"]
    counts = {}
    total = 0
    while total < 120 or total > 500:
        for i in range(6*3):
            num = random.randint(15,40)
            counts[programs[i]] = num
            total = sum(counts.values())
    return counts

#===================================================================================================
# Old Functions: Don't Use
def findRoom(totalStudents, course):
    """
    For use in findRooms()
    Returns the smallest room that can fit totalStudents
    """
    minimalEmptySeats = 100000
    bestRoom = False
    allRoomsFull = True

    for room in rooms:
        if (roomHours[room.ID] + course.termHours) > PROGRAMHOURS or course.hasLab != room.isLab: continue

        allRoomsFull = False

        emptySeats = room.capacity - totalStudents
        if emptySeats >= 0 and emptySeats < minimalEmptySeats:
            minimalEmptySeats = emptySeats
            bestRoom = room
    
    if allRoomsFull:
        print(course)
        ghostID = f"ghost-{len(ghostRooms) + 1}"
        ghostCapacity = totalStudents + (totalStudents % 6)
        ghostLab = course.hasLab
        ghostRoom = Classroom(ghostID, ghostCapacity, ghostLab)

        rooms.append(ghostRoom)
        ghostRooms.append(ghostRoom)
        roomHours[ghostID] = 0
        roomFill[ghostID] = []

        bestRoom = findRoom(totalStudents, course)
    
    return bestRoom

def splitLegions(legions):
    """
    Split a list of legions into 2 lists of legions
    """
    list1 = []
    list2 = []
    for i in range(len(legions)):
        if i%2 == 0: list1.append(legions[i])
        else:        list2.append(legions[i])
    
    return (list1, list2)

def bookLegions(legions, totalStudents, course):
    """
    For use in fillClassrooms()
    totalStudents is an int representing all students that must take that course
    program is a string id of a program and term, maybe make it an object later

    Finds the most efficient way to store the legions into a classroom
    """
    room = findRoom(totalStudents, course)

    if room == False:
        # There are no classrooms with enough hours and capacity to fit the students
        # Split into two and try again
        # *** Needs work, is not efficient if more than one split is required ***
        splitGroups = splitLegions(legions)

        totalStudents0 = 0
        for legionSize in splitGroups[0]:
            totalStudents0 += legionSize
        totalStudents1 = 0
        for legionSize in splitGroups[1]:
            totalStudents1 += legionSize
        
        bookLegions(splitGroups[0], totalStudents0, course)
        bookLegions(splitGroups[1], totalStudents1, course)
        return
        
    roomHours[room.ID] += course.termHours
    roomFill[room.ID].append(totalStudents)

def fillClassrooms(legions):
    """
    Fills classrooms with legions in courses
    Does not make a schedule, only checks if all students can fit

    Schedules one room until it is completely booked before moving on to the next
    """
    for program in programCoursesByTerm.keys():
    #for program in ["PM01", "PM02", "PM03", "BA01", "BA02", "BA03", "GLM01", "GLM02", "GLM03"]:

        totalStudents = 0
        for legionSize in legions[program]:
            totalStudents += legionSize
        
        for course in programCoursesByTerm[program]:
            bookLegions(legions[program], totalStudents, course)

#===================================================================================================
# New, cooler algorithm
def add_ghost_room(hasLab):
    ghostID = f"ghost-{len(ghostRooms) + 1}"
    ghostRoom = Classroom(ghostID, 30, hasLab)

    rooms.append(ghostRoom)
    ghostRooms.append(ghostRoom)
    roomHours["Core"][ghostID] = 0
    roomHours["Program"][ghostID] = 0

def check_room_hours(program, cohorts, isCore):
    temp_roomHours = roomHours[isCore].copy()
    for cohort_count in cohorts:
        for course in programCoursesByTerm[program]:
            scheduled = False
            for room in rooms:
                if temp_roomHours[room.ID] + course.termHours <= PROGRAMHOURS and room.isLab == course.hasLab:
                    temp_roomHours[room.ID] += course.termHours
                    scheduled = True
                    break
                
            if not scheduled:
                add_ghost_room(course.hasLab) 
                return True
    return False

def cohorts_fits(program, cohorts, isCore):
    global roomHours
    temp_roomHours = roomHours[isCore].copy()
    for cohort_count in cohorts:
        for course in programCoursesByTerm[program]:
            scheduled = False
            for room in rooms:
                if temp_roomHours[room.ID] + course.termHours <= PROGRAMHOURS and room.isLab == course.hasLab and room.capacity >= cohort_count:
                    temp_roomHours[room.ID] += course.termHours
                    scheduled = True
                    break
                
            if not scheduled: return False
    
    roomHours[isCore] = temp_roomHours.copy()
    return True

def fillPrograms(program_counts):

    for program in program_counts.keys():
        if programCoursesByTerm[program][0].isCore: isCore = "Core"
        else: isCore = "Program"
        total_size = program_counts[program]
        number_of_cohorts = 1
        cohorts = [total_size]

        scheduled = False
        while not scheduled:

            # Check if remaining rooms have enough time left
            # if not, add ghost room
            full_schedule = True
            while full_schedule:
                full_schedule = check_room_hours(program, cohorts, isCore)
                if full_schedule: 
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

    connection = create_connection(r".\database\database.db") 
    for room in ghostRooms:
        addClassroomItem(connection, room)
    close_connection(connection)
    
    

# TODO:
#   - 2 terms at a time
#   - Database integration

# Nice to have:
#   - Better cohort split algorithm
#   - Add rhyme and reason to ghostroom capacity in add_ghost_room()
#   - Extensive testing


#===================================================================================================
if __name__ == '__main__':
    x = "Donothing"
    # print(rooms, ghostRooms)
    # add_ghost_room(True)
    # print(rooms, ghostRooms)

    # print(rooms, ghostRooms)
    # print(check_room_hours("PM01", [36, 24]))
    # print(rooms, ghostRooms)

    # print(rooms, ghostRooms, roomHours)
    # print(cohorts_fits("PM01", [40, 24]))
    # print(rooms, ghostRooms, roomHours)

    # add_ghost_room(False)
    # for room in ghostRooms:
    #         connection = create_connection(r".\database\database.db")
    #         addClassroomItem(connection, room)
    #         close_connection(connection)
    program_counts = {}
    for key in programCoursesByTerm.keys():
        program_counts[key] = random.randint(18, 189)
    fillPrograms(program_counts)
    print(roomHours)
    print(ghostRooms)