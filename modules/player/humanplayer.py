from modules.player import playerinstance
from constants import strings as CONSTSTR
from random import randrange;
class HumanPlayer(playerinstance.PlayerInstance):
    def __init__(self, id, color, team, units, homeBase):
        super().__init__(id, color, team, units, homeBase)

    
    # Get the default player name from the list 
    def identifier(self, name=None):
        if(name is None):
            name = CONSTSTR.DEFAULT_UNNAMED[(len(CONSTSTR.DEFAULT_UNNAMED))]
        self.identifier = name 

    def team(self):
        return self.team
    
    # property getter
    def human(self):
        return True

    # property setter
    def color(self):
        return CONSTSTR.AVAILABLE_COLORS[self.color]

    #Score getter
    def score(self):
        return self.score
    
    # Score setter
    def score(self, value):
        self.score = value

    