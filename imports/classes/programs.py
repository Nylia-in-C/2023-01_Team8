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
    "BKC": ["ACCT 0201", "ACCT 0202", "ACCT 0203", "ACCT 0206", "ACCT 0210", "ACCT 0211", 
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
    