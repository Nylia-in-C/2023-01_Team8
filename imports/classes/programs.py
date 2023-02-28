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
            "ACCT 0208", "ACCT 9901"]
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
        return ( self.ID, self.courses )
       
        #testing purposes
    def printPrograms(self):
         print( self.createProgramItemInfo())


# Need to move this to the database
legionCounts = {"PM01" : 0, "PM02" : 0, "PM03" : 0,
                "BA01" : 0, "BA02" : 0, "BA03" : 0,
                "GLM01": 0, "GLM02": 0, "GLM03": 0, 
                "FS01" : 0, "FS02" : 0, "FS03" : 0, 
                "DXD01": 0, "DXD02": 0, "DXD03": 0,
                "BK01" : 0, "BK02" : 0, "BK03" : 0 }

# When database is implemented, needs to check if the 
@dataclass
class Legion(Program):
    cohorts: list = field(default_factory=list) #Bandaid solution for the "non-default follows default" error
    term: str = ""
    count: int = 0

    def __post_init__(self):
        Program.__post_init__(self)

        if self.term not in ["01", "02", "03"]:
            self.term = self.cohorts[0].termID

        if self.count < 1:
            legionCounts[self.ID + self.term] += 1
            self.count = "{:02d}".format(legionCounts[self.ID + self.term])

    def __repr__(self):
        return f"{self.ID}{self.term}{self.count} cohorts = {self.cohorts}"
    
    def createLegionItemInfo(self):
        """
        Returns a tuple of the Legion info
        Passed to database to load program into the database.
        """
        # May need to expand on self.cohorts, as each cohort will need to be loaded into the database
        return ( self.ID, self.term, self.count, self.cohorts, self.courses )

         
#testing purposes
# Dummy = Program('BKC', ["ACCT 0201", "ACCT 0202", "ACCT 0203", "ACCT 0206", "ACCT 0210", "ACCT 0211", 
#             "ACCT 0208", "ACCT 9901"])      
# Dummy.printPrograms() 
