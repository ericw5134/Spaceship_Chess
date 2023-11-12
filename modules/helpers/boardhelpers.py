import pygame
import modules.board.boardsquare as boardsquare
import modules.board.baseboardsquare as baseboardsquare
import modules.board.endboardsquare as endboardsquare
from constants import numerics as CONSTNUM
from constants import strings as CONSTSTR
from modules.player.spaceship import PurpleSpaceship, RedSpaceship, TealSpaceship, BlueSpaceship

def loadStartIndicatorImage(color):
    if color == "purple":
            return pygame.image.load(CONSTSTR.PURPLE_PLAYER_START_SPRITE_LOCATION).convert_alpha()
    elif color == "blue":
        return pygame.image.load(CONSTSTR.BLUE_PLAYER_START_SPRITE_LOCATION).convert_alpha()
    elif color == "red":
        return pygame.image.load(CONSTSTR.RED_PLAYER_START_SPRITE_LOCATION).convert_alpha()
    elif color == "teal":
        return pygame.image.load(CONSTSTR.TEAL_PLAYER_START_SPRITE_LOCATION).convert_alpha()

def buildEnding(squares, surface, color, team):
    for idx, coord in enumerate(squares):
        if (idx<5):
            square = boardsquare.BoardSquare(coord, color)
        else:
            square = endboardsquare.EndBoardSqure(coord, color, team)
        square.draw(surface)

def buildBase(squares, surface, color):
    for coord in squares:
        square = baseboardsquare.BaseBoardSquare(coord, color)
        square.draw(surface)

def buildBoardOrder(squares, surface):
    colors = [pygame.Color(125, 98, 140),pygame.Color(64, 94, 127),pygame.Color(134, 87, 99),pygame.Color(76, 124, 140)] # Purple, Blue, Red, Teal
    color_idx = 0
    for coord in squares:
        square = boardsquare.BoardSquare(coord, colors[color_idx])
        square.draw(surface)
        color_idx = (color_idx + 1) % 4 
    color_idx = 0

def buildStartIndicator(square, surface, color):
    start_sprite = loadStartIndicatorImage(color)
    x,y = square
    if square == CONSTNUM.PURPLESTARTINDICATOR or square == CONSTNUM.REDSTARTINDICATOR:
        pos = pygame.Rect((x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, CONSTNUM.BOXSIZE*2+2*CONSTNUM.OFFSET, CONSTNUM.BOXSIZE)
    elif square == CONSTNUM.BLUESTARTINDICATOR or square == CONSTNUM.TEALSTARTINDICATOR:
        pos = pygame.Rect((x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, CONSTNUM.BOXSIZE, CONSTNUM.BOXSIZE*2+2*CONSTNUM.OFFSET)

    surface.blit(start_sprite, start_sprite.get_rect(center=pos.center))

def createBoardSurf():
    board_surf = pygame.Surface((CONSTNUM.TILESIZE*CONSTNUM.BOARDSIZE, CONSTNUM.TILESIZE*CONSTNUM.BOARDSIZE), pygame.SRCALPHA,32)
    
    # Build board
    buildBoardOrder(CONSTNUM.BOARDORDER, board_surf)
    
    # Build the ending bit for each color
    buildEnding(CONSTNUM.PURPLEENDING, board_surf, pygame.Color(125, 98, 140), 'purple')
    buildEnding(CONSTNUM.BLUEENDING, board_surf, pygame.Color(64, 94, 127), 'blue')
    buildEnding(CONSTNUM.REDENDING, board_surf, pygame.Color(134, 87, 99), 'red')
    buildEnding(CONSTNUM.TEALENDING, board_surf, pygame.Color(76, 124, 140), 'teal')

    # Build the base for each color
    buildBase(CONSTNUM.PURPLEBASE, board_surf, pygame.Color(125, 98, 140))
    buildBase(CONSTNUM.BLUEBASE, board_surf, pygame.Color(64, 94, 127))
    buildBase(CONSTNUM.REDBASE, board_surf, pygame.Color(134, 87, 99))
    buildBase(CONSTNUM.TEALBASE, board_surf, pygame.Color(76, 124, 140))

    # Build start indicator for each color
    buildStartIndicator(CONSTNUM.PURPLESTARTINDICATOR, board_surf, 'purple')
    buildStartIndicator(CONSTNUM.BLUESTARTINDICATOR, board_surf, 'blue')
    buildStartIndicator(CONSTNUM.REDSTARTINDICATOR, board_surf, 'red')
    buildStartIndicator(CONSTNUM.TEALSTARTINDICATOR, board_surf, 'teal')

    return board_surf

def createBoard(players):

    # initializes board array
    board = []
    for y in range(CONSTNUM.BOARDSIZE):
        board.append([])
        for x in range(CONSTNUM.BOARDSIZE):
            board[y].append(None)

    # Populates each base with pieces
    
    for coords in CONSTNUM.PURPLEBASE:
        y = coords[0]
        x = coords[1]
        spaceship = PurpleSpaceship('blue',coords,0)
        players[0].spaceships.append(spaceship)
        board[y][x] = [spaceship]
    for coords in CONSTNUM.BLUEBASE:
        y = coords[0]
        x = coords[1]
        spaceship = BlueSpaceship('blue',coords,0)
        players[1].spaceships.append(spaceship)
        board[y][x] = [spaceship]
    for coords in CONSTNUM.REDBASE:
        y = coords[0]
        x = coords[1]
        spaceship = RedSpaceship('blue',coords,0)
        players[2].spaceships.append(spaceship)
        board[y][x] = [spaceship]
    for coords in CONSTNUM.TEALBASE:
        y = coords[0]
        x = coords[1]
        spaceship = TealSpaceship('blue',coords,0)
        players[3].spaceships.append(spaceship)
        board[y][x] = [spaceship]
    return board

# Chris: createBoard when game is being loaded
def createBoardLoad(players,boardpass):
    
    board = []
    for y in range(CONSTNUM.BOARDSIZE):
        board.append([])
        for x in range(CONSTNUM.BOARDSIZE):
            board[y].append(None)
    
    # initializes board array
    for i in range(0,17):
        for j in range(0,17):
            if boardpass[i][j] != None:
                if 'Purple' in boardpass[i][j]:
                    y = i 
                    x = j 
                    coords = (i,j)
                    spaceship = PurpleSpaceship('purple',coords,0)
                    players[0].spaceships.append(spaceship)
                    board[y][x] = [spaceship]
                if 'Blue' in boardpass[i][j] :
                    y = i 
                    x = j 
                    coords = (i,j)
                    spaceship = BlueSpaceship('blue',coords,0)
                    players[1].spaceships.append(spaceship)
                    board[y][x] = [spaceship]
                if 'Red' in boardpass[i][j] :
                    y = i 
                    x = j 
                    coords = (i,j)
                    spaceship = RedSpaceship('red',coords,0)
                    players[2].spaceships.append(spaceship)
                    board[y][x] = [spaceship]
                if 'Teal' in boardpass[i][j] :
                    y = i 
                    x = j 
                    coords = (i,j)
                    spaceship = TealSpaceship('Teal',coords,0)
                    players[3].spaceships.append(spaceship)
                    board[y][x] = [spaceship]
    return board
