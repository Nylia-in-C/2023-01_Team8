# attributes: 
# 1. Program id (string)
# 2. Term id (string)
# 3. cohort id (string)
# 4. Name  -> composite of Program ID, term ID, and cohort ID (string)
# 5. count -> number of students (int)


# To initialize: pass program ID, term ID, student count (cohort ID increments by 1),
# Name is created by concatenating these

class Cohort:

    cohortCounts = {"PM01" :  0, "PM02" :  0, "PM03" :  0,
                    "BA01" :  0, "BA02" :  0, "BA03" :  0,
                    "GLM01" : 0, "GLM02" : 0, "GLM03" : 0, 
                    "FS01" :  0, "FS02" :  0, "FS03" :  0, 
                    "DXD01" : 0, "DXD02" : 0, "DXD03" : 0,
                    "BK01" :  0, "BK02" :  0, "BK03" :  0}
    #Abbreviation for BookKeeping Certificate is not in specs, using "BK" for now

    def __init__(self, programID, termID, studentCount):
        #Increment cohorts
        Cohort.cohortCounts[programID + termID] += 1

        self.programID = programID
        self.termID = termID
        self.cohortID = "{:02d}".format(Cohort.cohortCounts[programID + termID])
        self.name = self.programID + self.termID + self.cohortID
        self.count = studentCount
