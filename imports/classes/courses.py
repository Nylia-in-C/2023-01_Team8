# represents a specific course 

# attributes: ID (string), title (string), pre-reqs (dict/list/graph maybe ? idk ),  
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