"""
Classroom contains data for a single classroom.
"""

from dataclasses import dataclass

@dataclass
class Classroom:
    ID: str
    capacity: int
    isLab: bool

    
    def __repr__(self):
        return f"{self.ID} has space for: {self.capacity} and is lab?: {self.isLab}"

    def createClassroomItemInfo(self):
        """
        Returns an item string of the objects contents.
        "ClassID , Capacity, IsLab"
        Passed to database to load class into the database.
        """
        return f" '{self.ID}', {self.capacity}, {self.isLab} "