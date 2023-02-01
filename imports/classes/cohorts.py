from dataclasses import dataclass

# Count of cohorts for autoincrement in class
cohortCounts = {"PM01" : 0, "PM02" : 0, "PM03" : 0,
                "BA01" : 0, "BA02" : 0, "BA03" : 0,
                "GLM01": 0, "GLM02": 0, "GLM03": 0, 
                "FS01" : 0, "FS02" : 0, "FS03" : 0, 
                "DXD01": 0, "DXD02": 0, "DXD03": 0,
                "BK01" : 0, "BK02" : 0, "BK03" : 0 }

@dataclass
class Cohort:
    programID: str
    termID: str
    count: int

    def __post_init__(self):
        #Increment cohorts
        cohortCounts[self.programID + self.termID] += 1
        self.cohortID = "{:02d}".format(cohortCounts[self.programID + self.termID])

        self.name = self.programID + self.termID + self.cohortID
    
    def __repr__(self):
        return f"{self.name} students: {self.count}"

    def createItemInfo(self):
        """
        Returns an item string of the objects contents.
        "ProgID, TermID, CohortID, Name, Count"
        Passed to database to load cohort into the database.
        """
        return f" '{self.programID}', {self.termID}, {self.cohortID}, '{self.name}', {self.count} "