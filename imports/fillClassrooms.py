
#===================================================================================================
# Imports
import random
from classes.classrooms import *
from classes.cohorts    import *
from classes.courses    import *
from classes.programs   import *
from create_cohorts     import *

#===================================================================================================
# Setup
PROGRAMHOURS = 2*13*9 #days*weeks*hours
#PROGRAMHOURS = 60
#COREHOURS

courseHours = {
    "PRDV 0201": 21, "PRDV 0202": 14, "PRDV 0203": 21, 
    "PRDV 0204": 14, "PRDV 0205": 21, "PCOM 0130": 21, "PRDV 0206": 14, 
    "PRDV 0207": 14, "PCOM 0131": 39,
    "PRDV 0640": 21, "PRDV 0652": 14, "PRDV 0653": 21, "PRDV 0642": 14, "PRDV 0644": 21, 
    #Correct up to this point
    "PRDV 0648": 21, "PCOM 0140": 21, "PRDV 0646": 21, "PCOM 0141": 21,
    "SCMT 0501": 21, "SCMT 0502": 21, "PRDV 0304": 21, "SCMT 9901": 21, "SCMT 0503": 21,
    "SCMT 0504": 21, "SCMT 9902": 21, "SCMT 0505": 21, "PCOM 0151": 21,
    "CMSK 0150": 21, "CMSK 0151": 21, "CMSK 0152": 21, "CMSK 0157": 21, "CMSK 0154": 21, 
    "CMSK 0153": 21, "CMSK 0200": 21, "CMSK 0201": 21, "CMSK 0203": 21, "CMSK 0202": 21, "PCOM 0160": 21,
    "AVDM 0165": 21, "DXDI 0101": 21, "DXDI 0102": 21, "AVDM 0170": 21, "AVDM 0138": 21, "DXDI 0103": 21, 
    "DXDI 0104": 21, "AVDM 0238": 21, "AVDM 0270": 21, "DXDI 9901": 21,
    "ACCT 0201": 21, "ACCT 0202": 21, "ACCT 0203": 21, "ACCT 0206": 21, "ACCT 0210": 21, "ACCT 0211": 21, 
    "ACCT 0208": 21, "ACCT 9901": 21
}

programCoursesByTerm = {
    "PM01":  [Course("PRDV 0201", "NA", 21, 2, False, False, False), Course("PRDV 0202", "NA", 14, 2, False, False, False), Course("PRDV 0203", "NA", 21, 2, False, False, False)], 
    "PM02":  [Course("PRDV 0204", "NA", 14, 2, False, False, False), Course("PRDV 0205", "NA", 21, 2, False, False, False), Course("PCOM 0130", "NA", 21, 2, False, False, False), Course("PRDV 0206", "NA", 14, 2, False, False, False)], 
    "PM03":  [Course("PRDV 0207", "NA", 14, 2, False, False, False), Course("PCOM 0131", "NA", 39, 2, False, False, False)],
    #Split into terms up to this point
    "BA01":  ["PRDV 0640", "PRDV 0652", "PRDV 0653", "PRDV 0642", "PRDV 0644", 
              "PRDV 0648", "PCOM 0140", "PRDV 0646", "PCOM 0141"],
    "GLM01": ["SCMT 0501","SCMT 0502","PRDV 0304","SCMT 9901","SCMT 0503",
              "SCMT 0504","SCMT 9902","SCMT 0505","PCOM 0151"],
    "FS01":  ["CMSK 0150", "CMSK 0151", "CMSK 0152", "CMSK 0157", "CMSK 0154", 
              "CMSK 0153", "CMSK 0200", "CMSK 0201", "CMSK 0203", "CMSK 0202", "PCOM 0160"],
    "DXD01": ["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103", 
              "DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"],
    # Program ID for book keeping certificate
    "BKC01": ["ACCT 0201", "ACCT 0202", "ACCT 0203", "ACCT 0206", "ACCT 0210", "ACCT 0211", 
              "ACCT 0208", "ACCT 9901"]
}

rooms = [Classroom("11-458", 40, False),
         Classroom("11-533", 36, False), 
         Classroom("11-534", 36, False),
         Classroom("11-430", 30, False), 
         Classroom("11-320", 30, False),
         Classroom("11-560", 24, False),
         Classroom("11-562", 24, False),
         Classroom("11-564", 24, False)]

ghostRooms = []

roomHours = {"11-458": 0,
             "11-533": 0, 
             "11-534": 0,
             "11-430": 0, 
             "11-320": 0,
             "11-560": 0,
             "11-562": 0,
             "11-564": 0}

roomFill  = {"11-458": [],
             "11-533": [], 
             "11-534": [],
             "11-430": [], 
             "11-320": [],
             "11-560": [],
             "11-562": [],
             "11-564": []}

Lab = Classroom("11-532", 30, True) 

#===================================================================================================
# Functions
def random_students_by_term():
    '''
    Randomly generates a dictionary mapping programIDs to their student counts (testing purposes only)
    '''
    programs = ["PM01",  "PM02",  "PM03",
                "BA01",  "BA02",  "BA03", 
                "GLM01", "GLM02", "GLM03", 
                "FS01",  "FS02",  "FS03", 
                "DXD01", "DXD02", "DXD03", 
                "BK01",  "BK02",  "BK03"]
    counts = {}
    total = 0
    while total < 120 or total > 500:
        for i in range(6*3):
            num = random.randint(15,40)
            counts[programs[i]] = num
            total = sum(counts.values())
    return counts

def findRoom(totalStudents, hours):
    """
    For use in findRooms()
    Returns the smallest room that can fit totalStudents
    """
    minimalEmptySeats = 100000
    bestRoom = False
    allRoomsFull = True

    for room in rooms:
        if (roomHours[room.ID] + hours) > PROGRAMHOURS: continue
        allRoomsFull = False

        emptySeats = room.capacity - totalStudents
        if emptySeats >= 0 and emptySeats < minimalEmptySeats:
            minimalEmptySeats = emptySeats
            bestRoom = room
    
    if allRoomsFull:
        ghostID = f"ghost-{len(ghostRooms) + 1}"
        ghostCapacity = 40
        ghostRoom = Classroom(ghostID, ghostCapacity, False)

        rooms.append(ghostRoom)
        ghostRooms.append(ghostRoom)
        roomHours[ghostID] = 0
        roomFill[ghostID] = []

        bestRoom = findRoom(totalStudents, hours)
    
    return bestRoom

def splitCohorts(cohorts):
    """
    Split a list of cohorts into 2 lists of cohorts
    """
    list1 = []
    list2 = []
    for i in range(len(cohorts)):
        if i%2 == 0: list1.append(cohorts[i])
        else:        list2.append(cohorts[i])
    
    return (list1, list2)

def bookCohorts(cohorts, totalStudents, course):
    """
    For use in fillClassrooms()
    totalStudents is an int representing all students that must take that course
    program is a string id of a program and term, maybe make it an object later

    Finds the most efficient way to store the cohorts into a classroom
    """

    room = findRoom(totalStudents, course.termHours)
    if room == False:
        # There are no classrooms with enough hours and capacity to fit the students
        # Split into two and try again
        splitGroups = splitCohorts(cohorts)

        totalStudents0 = 0
        for cohortSize in splitGroups[0]:
            totalStudents0 += cohortSize
        totalStudents1 = 0
        for cohortSize in splitGroups[1]:
            totalStudents1 += cohortSize
        
        bookCohorts(splitGroups[0], totalStudents0, course)
        bookCohorts(splitGroups[1], totalStudents1, course)
        return
        
    roomHours[room.ID] += course.termHours
    roomFill[room.ID].append(totalStudents)

def fillClassrooms(cohorts):
    """
    Fills classrooms with cohorts in courses
    Does not make a schedule, only checks if all students can fit

    Schedules one room until it is completely booked before moving on to the next
    """
    for program in ["PM01", "PM02", "PM03"]:
        totalStudents = 0
        for cohortSize in cohorts[program]:
            totalStudents += cohortSize
        
        for course in programCoursesByTerm[program]:
            bookCohorts(cohorts[program], totalStudents, course)
        
#===================================================================================================
if __name__ == '__main__':
    cohorts = create_cohort_dict(random_students_by_term())
    fillClassrooms(cohorts)

    print(roomFill, roomHours)

