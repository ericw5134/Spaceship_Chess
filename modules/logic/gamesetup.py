from random import randrange
from constants import numerics as CONSTNUM
from constants import strings as CONSTSTR
from modules.player import humanplayer, aiplayer
from modules.player import spaceship
import copy
#builder for gamesetup
# Currently it will just be set to 1 ai, 1 human until further implementation
# Builder class sets up the player object both AI and human and instantiates the Unit objects that the player/ai will move
class GameSetup():
    def create_players(self,ai, id):
        if(ai):
           return aiplayer.AIPlayer(self.available_colors[id], id, 4, self.available_colors[id])
        else:
            return humanplayer.HumanPlayer(self.available_colors[id], id, 4, self.available_colors[id])
    
    #Takes objects by ref
    def create_teams(self):
        team_setup = dict()
        player_setup = dict()
        players_created = 0
        random_number = randrange(1,100)
        self.base_index = (random_number % 4)
        color_index = (self.base_index + self.total)%4
        
        # For every intended AI created use their creation order as a numeric ID
        # Instantiate an AiPlayer object and put it in a dictionary
        # Then put that into a higher level dictionary to order teams 
        while self.total > 0 and self.ai > 0:
            obj = aiplayer.AIPlayer(players_created, self.available_colors[color_index], color_index, 4, CONSTNUM.BASE_TUPLE[color_index])
            player_setup.update({players_created:object})
            self.create_planes(players_created, color_index)
            team_setup.update({color_index:player_setup})
            color_index = (color_index+1)%4
            self.aiinstance+=1
            players_created+=1
            if self.aiinstance == self.ai:
                break
        
        # Same as above but instantiate a HumanPlayer object
        while self.total > 0 and self.human > 0:
            obj = humanplayer.HumanPlayer(players_created, self.available_colors[color_index], color_index, 4, CONSTNUM.BASE_TUPLE[color_index])
            player_setup.update({players_created:object})
            self.create_planes(players_created, color_index)
            team_setup.update({color_index:player_setup})
            color_index = (color_index+1)%4
            self.humaninstance+=1
            players_created += 1
            if self.humaninstance == self.human:
                break
        self.dataDict = team_setup   

        
    def create_planes(self, playerid, color_index, numplanes = None):
        spaceship_obj = None
        spaceship_count = 0
        spaceshipDict = dict()

        if(numplanes is None):
            numplanes = CONSTNUM.DEFAULT_NUMBER_OF_PLANES
        # create a singular plane instance using the spaceship prototype in spaceship.py
        if color_index == CONSTNUM.TEAL_TEAM_INDEX:
            spaceship_obj = spaceship.TealSpaceship(color_index, CONSTNUM.BASE_TUPLE[color_index], playerid)
        elif color_index == CONSTNUM.PURPLE_TEAM_INDEX:
            spaceship_obj = spaceship.PurpleSpaceship(color_index, CONSTNUM.BASE_TUPLE[color_index], playerid)
        elif color_index == CONSTNUM.BLUE_TEAM_INDEX:
            spaceship_obj = spaceship.BlueSpaceship(color_index, CONSTNUM.BASE_TUPLE[color_index], playerid)
        elif color_index == CONSTNUM.RED_TEAM_INDEX:
            spaceship_obj = spaceship.RedSpaceship(color_index, CONSTNUM.BASE_TUPLE[color_index], playerid)
        else:
            raise('Invalid color_index for create_planes: ',color_index)
        
        # Put the spaceship into a data structure for later access
        spaceshipDict.update({spaceship_count:spaceship_obj})
        spaceship_count+=1
        # then use prototype clone to create the remaining instances
        tmpObj = None
        for i in range(CONSTNUM.DEFAULT_NUMBER_OF_PLANES):
            tmpObj = spaceship_obj.clone()
            spaceshipDict.update({spaceship_count:spaceship_obj})
        
        self.playerDict.update({playerid:spaceshipDict})

    def get_player_info(self):
        return copy.deepcopy(self.playerDict)
   
    def __init__(self, total, human, ai):
        #[teal purple blue red]
        self.available_colors = CONSTSTR.AVAILABLE_COLORS
        self.human = human
        self.ai = ai
        self.humaninstance = 0
        self.aiinstance = 0
        self.base_index = 0
        self.iterate = 0
        self.total = total
        self.dataDict = dict()
        self.playerDict = dict()
        
        if(human + ai != total):
            raise('Incorrect values for human/ai player')
        
        self.create_teams()
        