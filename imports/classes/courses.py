# represents a specific course 

# attributes: ID (string), title (string), pre-reqs (dict/list/graph maybe ? idk ),  
#             term hours (int), isCore (bool), timeSlot (int), isOnline (bool)

from dataclasses import field, dataclass

preReqs = {
    "course1": ["preReq1", "preReq2"],
    "course2": ["prereq1", "prereq2"],
    "course3": ["prereq1", "prereq2", "preReq3"]
}

@dataclass
class Course:
    ID: str
    title: str
    termHours: str
    duration: int
    isCore: bool
    isOnline: bool
    hasLab: bool
    # either list of strings indicating preReq course titles, or list of Course objects
    preReqs: list = field(default_factory=list)
    
    def __post_init__(self):
        if self.ID not in preReqs.keys():
            self.preReqs = []
        self.preReqs = preReqs[self.ID]