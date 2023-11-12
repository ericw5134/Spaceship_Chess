from abc import ABC, abstractmethod 
# Abstract factory for the player 
class PlayerInstance(ABC):

    def __init__(self, id, color, team, units, homeBase):
        self.playerID = id
        self.color = color
        self.team = team
        self.units = units
        self.homeBase = homeBase
        self.score = 0
        self.identifer = None

    @property
    @abstractmethod
    def human(self):
        pass

    # getter property for ID
    @property
    @abstractmethod
    def identifier(self):
        pass
    
    # getter property for team
    @property
    @abstractmethod
    def team(self):
        pass

    # getter property for color
    @property
    @abstractmethod
    def color(self):
        pass

    # getter property for score
    @property
    @abstractmethod
    def score(self):
        pass
    
    # setter property for score
    @property
    @abstractmethod
    def score(self, value):
        pass

    