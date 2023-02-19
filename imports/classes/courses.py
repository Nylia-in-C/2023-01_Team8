# represents a specific course 

# attributes: ID (string), title (string), pre-reqs (dict ),  
#             term hours (int), isCore (bool), timeSlot (int), isOnline (bool)

from dataclasses import field, dataclass

# Directed graph representing course prerequisites (might change to Course objects later)
# note: only program-specific courses have prerequisites
preReqs = {
    "CMSK 1052": ["CMSK 0151"],
    "CMSK 1053": ["CMSK 1052", "CMSK 0157"],
    "CMSK 0200": ["CMSK 0154"],
    "CMSK 0201": ["CMSK 0200"],  # 0154 is omitted since it's already a preReq for 0200
    "CMSK 0203": ["CMSK 0201"],
    "DXDI 0102": ["DXDI 0101"],
    "DXDI 0103": ["DXDI 0102"],
    "DXDI 0104": ["DXDI 0103"],
}

@dataclass
class Course:
    ID: str
    title: str
    termHours: int
    duration: int
    isCore: bool
    isOnline: bool
    hasLab: bool
    # list of strings indicating preReq course titles
    preReqs: list = field(default_factory=list)
    
    # called immediately after object is created & attributes are initialized
    def __post_init__(self):
        if self.ID in preReqs.keys():
            self.preReqs = preReqs[self.ID]
        else:
            self.preReqs = []

    def createCourseItemInfo(self):
        """
        Returns a tuple of the Course information.
        CourseID, title, termHours, duration, isCore, isOnline, hasLab, preReq 
        Passed to database to load program into the database.
        """
        preReqsString = ""
        i = len(self.preReqs)-1
        for Req in self.preReqs:
            if i==0:
                preReqsString = preReqsString + self.preReqs[i]
                i=i-1
            else:
                preReqsString = preReqsString + self.preReqs[i] + ', '
                i = i-1
        return ( self.ID, self.title, self.termHours, self.duration, self.isCore, self.isOnline, self.hasLab, preReqsString )
       
        #testing purposes
    def printCourse(self):
         print( self.createCourseItemInfo())


class Section(Course):
    pass


#testing purposes
# Dummy = Course('CMSK 1053', 'theTitle', 40, 45, 0,1,0, ["CMSK 1052", "CMSK 0157"])      
# Dummy.printCourse()
#subDummy = Section('CMSK 1053', 'theTitle', 40, 45, 0,1,0, ["CMSK 1052", "CMSK 0157"])
#print(subDummy)