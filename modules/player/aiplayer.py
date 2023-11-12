from modules.player import playerinstance
class AIPlayer(playerinstance.PlayerInstance):
    def __init__(self, id, color, team, units, homeBase):
        super().__init__(id, color, team, units, homeBase)
    
  
    # Set name to AI #ID 
    def identifier(self):
        name = "AI #"+str(id)
        self.identifier = name

    def team(self):
        return self.team

    # property getter
    def human(self):
        return False

    # property setter
    def color(self):
        return CONSTSTR.AVAILABLE_COLORS[self.color]

    #Score getter
    def score(self):
        return self.score
    
    # Score setter
    def score(self, value):
        self.score = value

    