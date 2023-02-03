from classes.classrooms import *
from classes.cohorts    import *
from classes.courses    import *
from classes.programs   import *

PROGRAMHOURS = 2*13*9 #days*weeks*hours
#COREHOURS

programs = []
for key in programCourses.keys():
    programs.append(Program(key))

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

Classrooms = [Classroom("11-458", 40, False),
              Classroom("11-533", 36, False), 
              Classroom("11-534", 36, False),
              Classroom("11-430", 30, False), 
              Classroom("11-320", 30, False),
              Classroom("11-560", 24, False),
              Classroom("11-562", 24, False),
              Classroom("11-564", 24, False)]

Lab = Classroom("11-532", 30, True) 