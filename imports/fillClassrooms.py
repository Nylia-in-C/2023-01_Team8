
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

rooms = [Classroom("11-458", 12, False),
         Classroom("11-533", 36, False), 
         Classroom("11-534", 36, False),
         Classroom("11-430", 30, False), 
         Classroom("11-320", 30, False),
         Classroom("11-560", 24, False),
         Classroom("11-562", 24, False),
         Classroom("11-564", 24, False)]

roomHours = {"11-458": 0,
             "11-533": 0, 
             "11-534": 0,
             "11-430": 0, 
             "11-320": 0,
             "11-560": 0,
             "11-562": 0,
             "11-564": 0}

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

def findRoom(roomCounter, course):
    """
    For use in fillClassrooms()
    roomCounter is an iterative variable for the rooms list
    course is a Course object

    Adds the course term hours to the rooms booked hours, and if
    the room is full, 
    """

def fillClassrooms(cohorts):
    """
    Fills classrooms with cohorts in courses
    Does not make a schedule, only checks if all students can fit

    Schedules one room until it is completely booked before moving on to the next
    """
    roomCounter = 0
    room = rooms[roomCounter]
    roomTotal = 0
    print(f"Room {room}")

    for term in ["PM01", "PM02", "PM03"]:
        print(f"Scheduling program {term}")
        for course in programCoursesByTerm[term]:
            print(f"Scheduling course {course}")
            while roomHours[room.ID] + course.termHours >= PROGRAMHOURS:
                # Find a room with enough hours
                roomCounter += 1
                room = rooms[roomCounter]
                print(f"Room {room.ID} hours: {roomHours[room.ID]}/{PROGRAMHOURS}")
            
            for cohortSize in cohorts[term]:
                print(f"Cohort of {cohortSize} students make {roomTotal + cohortSize} in capacity of {room.capacity}")
                if (cohortSize + roomTotal) <= room.capacity:
                    # Can fit one more cohort in there
                    roomTotal += cohortSize
                    print(f"Putting cohort of size {cohortSize} to {room.ID}")
                else:
                    # New course offering
                    roomHours[room.ID] += course.termHours
                    print(f"Room full at {roomTotal} students. {roomHours[room.ID]}/{PROGRAMHOURS} hours")

                    while roomHours[room.ID] + course.termHours >= PROGRAMHOURS:
                        # Find a room with enough hours
                        roomCounter += 1
                        room = rooms[roomCounter]
                        print(f"Room {room.ID} hours: {roomHours[room.ID]}/{PROGRAMHOURS}")
                    
                    # Put cohort in the next room
                    roomTotal = cohortSize
                    print(f"Putting cohort of {cohortSize} into {room.ID} for {roomTotal} students in capacity of {room.capacity}")
            
            # Book room for last course offering
            print(f"Total students: {roomTotal}")
            roomHours[room.ID] += course.termHours
            print(f"Room {room.ID} hours: {roomHours[room.ID]}/{PROGRAMHOURS}")
            roomTotal = 0

cohorts = create_cohort_dict(random_students_by_term())
fillClassrooms(cohorts)