from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Team:
    constructorId: int
    constructorRef:str
    name:str
    nationality:str
    url:str

    risultati_per_anno: dict = field(default_factory=dict)
    gare_completate: int = 0

    #PER LA RICORSIONE:
    gare_totali: int = 0
    def __hash__(self):
        return hash(self.constructorId)

    def __eq__(self, other):
        if isinstance(other, Team):
            return self.constructorId == other. constructorId
        return False

    def __repr__(self):
        return (f"{self.name} ({self. constructorId}) ")
                # if self.year is not None else 'N/D'})")