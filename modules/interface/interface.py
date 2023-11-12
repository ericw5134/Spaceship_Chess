from modules.logic import gamesetup
from typing import Dict
## This is the bridge structure that binds the abstraction and implemention 
class Interface():
        def __init__(self):
            self.playerInfo = None
            self.teamSetup = None
        
       
        ## DEBUG
        def printDictionary(self):
               pass
        
        def updatePlayerInformation(self, dict):
            self.playerInfo = dict
        
        def gamesetup(self):
                pass
        
        def render(self):
                pass