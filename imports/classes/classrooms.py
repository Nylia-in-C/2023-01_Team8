# attributes: ID (string), capacity (int), isLab (bool)

from dataclasses import dataclass

@dataclass
class Classroom:
    ID: str
    capacity: int
    isLab: bool