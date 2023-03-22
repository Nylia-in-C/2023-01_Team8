# class that represents one of seven possible programs

# attributes: ID (string), courses (list of strings indicating courses unique to the program)

from dataclasses import field, dataclass

programCourses = {
    "PM":  ["PRDV 0201", "PRDV 0202", "PRDV 0203", "PRDV 0204", 
            "PRDV 0205", "PCOM 0130", "PRDV 0206", "PRDV 0207", "PCOM 0131"],
    "BA":  ["PRDV 0640", "PRDV 0652", "PRDV 0653", "PRDV 0642", "PRDV 0644", 
            "PRDV 0648", "PCOM 0140", "PRDV 0646", "PCOM 0141"],
    "GLM": ["SCMT 0501","SCMT 0502","PRDV 0304","SCMT 9901","SCMT 0503",
            "SCMT 0504","SCMT 9902","SCMT 0505","PCOM 0151"],
    "FS":  ["CMSK 0150", "CMSK 0151", "CMSK 0152", "CMSK 0157", "CMSK 0154", 
            "CMSK 0153", "CMSK 0200", "CMSK 0201", "CMSK 0203", "CMSK 0202", "PCOM 0160"],
    "DXD": ["AVDM 0165", "DXDI 0101", "DXDI 0102", "AVDM 0170", "AVDM 0138", "DXDI 0103", 
            "DXDI 0104","AVDM 0238","AVDM 0270","DXDI 9901"],
    # Program ID for book keeping certificate
    "BK": ["ACCT 0201", "ACCT 0202", "ACCT 0203", "ACCT 0206", "ACCT 0210", "ACCT 0211", 
            "ACCT 0208", "ACCT 9901"],
    #CORE COURSES
    'PCOM':["PCOM 0101","PCOM 0105", "PCOM 0107","CMSK 0233","CMSK 0235","PCOM 0102","PCOM 0201","PCOM 0108","PCOM 0202","PCOM 0103","PCOM 0109"],
    'BCOM':["PCOM 0203","SUPR 0751","PCOM 0204","CMSK 0237","SUPR 0837","SUPR 0841","SUPR 0821","SUPR 0822","SUPR 0718","SUPR 0836","AVDM 0199","PCOM 0106","PCOM 0205","PCOM TBD","PCOM 0207","SUPR 0863","PCOM 0206","AVDM 0260"]
}

@dataclass
class Program:
    ID: str
    courses: list = field(default_factory=list)
    
    # called immediately after object is created & attributes are initialized
    def __post_init__(self):
        if self.ID not in programCourses.keys():
            raise ValueError(f"{self.ID} is not a valid program ID")
        self.courses = programCourses[self.ID]

    def createProgramItemInfo(self):
        """
        Returns a tuple of the ProgramID and a list of the courses.
        "ProgID, Courses"
        Passed to database to load program into the database.
        """
        return ( self.ID, self.courses)
       
        #testing purposes
    def printPrograms(self):
         print( self.createProgramItemInfo())


# Need to move this to the database
'''
cohortCounts = {"PM01" : 0, "PM02" : 0, "PM03" : 0,
                "BA01" : 0, "BA02" : 0, "BA03" : 0,
                "GLM01": 0, "GLM02": 0, "GLM03": 0, 
                "FS01" : 0, "FS02" : 0, "FS03" : 0, 
                "DXD01": 0, "DXD02": 0, "DXD03": 0,
                "BK01" : 0, "BK02" : 0, "BK03" : 0 }
'''

# When database is implemented, needs to check if the 
@dataclass
class Cohort(Program):
    """
    A collection of legions for a certain program and term, which are taking classes together.

    ***legions must be declared on class creation!***
    ***It will not function properly if you do not specify legions***

    cohortCounts needs to be replaced with a sql call to the database.
    """
    legions: list = field(default_factory=list) #Bandaid solution for the "non-default follows default" error
    term: int = 0
    cohortID: str = ""

    def __post_init__(self):
        Program.__post_init__(self)

    def __repr__(self):
        return f"{self.ID}{self.term}{self.cohortID} legions = {self.legions}"
    
    def createCohortItemInfo(self):
        """
        Returns a tuple of the Cohort info
        Passed to database to load program into the database.

        self.legions is a list of legion objects and should be handled accordingly
        """
        legionString = ""
        i = len(self.legions)-1
        for Leg in self.legions:
            if i==0:
                legionString = legionString + self.legions[i]
                i=i-1
            else:
                legionString = legionString + self.legions[i] + '. '
                i = i-1

        courseString = ""
        i = len(self.courses)-1
        for Leg in self.courses:
            if i==0:
                courseString = courseString + self.courses[i]
                i=i-1
            else:
                courseString = courseString + self.courses[i] + '. '
                i = i-1
        # May need to expand on self.legions, as each legion will need to be loaded into the database
        
        return ( self.ID, self.term, self.cohortID, legionString, courseString )

         
#testing purposes
# Dummy = Program('BK', ["ACCT 0201", "ACCT 0202", "ACCT 0203", "ACCT 0206", "ACCT 0210", "ACCT 0211", 
#             "ACCT 0208", "ACCT 9901"])      
# Dummy.printPrograms() 
