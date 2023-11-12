from abc import ABC, abstractmethod
import copy
from constants import numerics as CONSTNUM
# prototype class
# Spaceship will use clone to produce help produce multiple identical unique objects
class Spaceship(ABC):
    def __init__(self, color, location, team):
        self.color = None
        self.location = None
        self.team = None
        self.isInBase = True
        self.isInEnding = False
        self.movable_squares = []
        self.basePos = None
        self.movable = False
        self.current = -1
    
    @abstractmethod
    def clone(self):
        pass

# inheritant classes

class PurpleSpaceship(Spaceship):
    def __init__(self, color, location, team):
        super().__init__(color, location, team)
        self.color = 'purple'
        self.location = location
        self.basePos = location
        self.team = 0
    
    def clone(self):
        return copy.deepcopy(self)

class BlueSpaceship(Spaceship):
    def __init__(self, color, location, team):
        super().__init__(color, location, team)
        self.color = 'blue'
        self.location = location
        self.basePos = location
        self.team = 1
        
    
    def clone(self):
        return copy.deepcopy(self)

class RedSpaceship(Spaceship):
    def __init__(self, color, location, team):
        super().__init__(color, location, team)
        self.color = 'red'
        self.location = location
        self.basePos = location
        self.team = 2
    
    def clone(self):
        return copy.deepcopy(self)

class TealSpaceship(Spaceship):
    def __init__(self, color, location, team):
        super().__init__(color, location, team)
        self.color = 'teal'
        self.location = location
        self.basePos = location
        self.team = 3
    
    def clone(self):
        return copy.deepcopy(self)