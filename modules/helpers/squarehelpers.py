import pygame
from constants.globalvars import BOARD_POS
from constants import numerics as CONSTNUM
def getSquareUnderMouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // CONSTNUM.TILESIZE) for v in mouse_pos]
    if (isLongTile(x,y)):
        if(((y==1 or y==16) and (x>=4 and x<=12))):
            if (y==1):
                y=0
            elif(y==16):
                y=15
        elif(((x==1 or x==16) and (y>=4 and y<=12))):
            if (x==1):
                x=0
            elif(x==16):
                x=15
    try: 
        if x >= 0 and y >= 0 and isValidSquare(x,y): return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None

def isLongTile(x,y):
    if ((y==0 or y==1 or y==15 or y==16) and (x>=4 and x<=12)) or ((x==0 or x==1 or x==15 or x==16) and (y>=4 and y<=12)):
        return True
    else:
        return False

def isValidSquare(x,y):
    coords = (y,x)
    if ((coords in CONSTNUM.BOARDORDER) or (coords in CONSTNUM.PURPLEENDING) or (coords in CONSTNUM.BLUEENDING) or (coords in CONSTNUM.REDENDING) or (coords in CONSTNUM.TEALENDING) or (coords in CONSTNUM.PURPLEBASE) or (coords in CONSTNUM.BLUEBASE) or (coords in CONSTNUM.REDBASE) or (coords in CONSTNUM.TEALBASE)):
        return True
    elif (isLongTile(y,x)):
        return True
    else: 
        return False
    
def isEndingSquare(x,y):
    coords = (y,x)
    if (coords in CONSTNUM.PURPLEENDING or coords in CONSTNUM.BLUEENDING or coords in CONSTNUM.REDENDING or coords in CONSTNUM.TEALENDING):
        return True
    else:
        return False
    
def isLastSquare(x,y):
    coords = (y,x)
    if (coords in CONSTNUM.LASTSQUARES):
        return True
    else:
        return False

# Using Launchsquare instead of start square
# def getStartSquare(player):
#     if player.color == "purple":
#        return (CONSTNUM.BOARDORDER[CONSTNUM.PURPLESTART],CONSTNUM.PURPLESTART)
#     elif player.color == "blue":
#         return (CONSTNUM.BOARDORDER[CONSTNUM.BLUESTART],CONSTNUM.BLUESTART)
#     elif player.color == "red":
#         return (CONSTNUM.BOARDORDER[CONSTNUM.REDSTART],CONSTNUM.REDSTART)
#     elif player.color == "teal":
#         return (CONSTNUM.BOARDORDER[CONSTNUM.TEALSTART],CONSTNUM.TEALSTART)
    
def getLaunchSquare(player):
    if player.color == "purple":
       return (CONSTNUM.PURPLELAUNCHSQUARE,CONSTNUM.PURPLESTART-1)
    elif player.color == "blue":
        return (CONSTNUM.BLUELAUNCHSQUARE,CONSTNUM.BLUESTART-1)
    elif player.color == "red":
        return (CONSTNUM.REDLAUNCHSQUARE,CONSTNUM.REDSTART-1)
    elif player.color == "teal":
        return (CONSTNUM.TEALLAUNCHSQUARE,CONSTNUM.TEALSTART-1)

def getEndSquare(player):
    if player.color == "purple":
       return CONSTNUM.PURPLEEND
    elif player.color == "blue":
       return CONSTNUM.BLUEEND
    elif player.color == "red":
        return CONSTNUM.REDEND
    elif player.color == "teal":
        return CONSTNUM.TEALEND
    
def getEndingSquares(player):
    if player.color == "purple":
       return CONSTNUM.PURPLEENDING
    elif player.color == "blue":
       return CONSTNUM.BLUEENDING
    elif player.color == "red":
        return CONSTNUM.REDENDING
    elif player.color == "teal":
        return CONSTNUM.TEALENDING

def getNewPos(spaceship, roll, player):
    current_pos = spaceship.current
    new_pos = (spaceship.current + roll) % CONSTNUM.BOARDMODULO
    end_index = getEndSquare(player)
    # Handles Teal Seperately

    if (spaceship.isInEnding == True):
        squares = getEndingSquares(player)
        spaceship.movable_squares.append((squares[current_pos+roll],current_pos+roll))
        return
    
    if (spaceship.current!=-1):
        if (player.color == "teal"):
            if (current_pos>50 or current_pos<=4) and (new_pos>end_index):
                moves = new_pos-end_index 
                squares = getEndingSquares(player)
                spaceship.movable_squares.append((squares[moves-1],moves-1))
                return
        else:
            if (current_pos<=end_index) and (new_pos>end_index):
                moves = new_pos-end_index
                squares = getEndingSquares(player)
                spaceship.movable_squares.append((squares[moves-1],moves-1))
                return squares[moves-1]

    if roll == 6:
        if spaceship.isInBase == True:
            start_square, index = getLaunchSquare(player)
            spaceship.movable_squares.append((start_square,index))
        else:
            spaceship.movable_squares.append((CONSTNUM.BOARDORDER[new_pos],new_pos))
    else:
        spaceship.movable_squares.append((CONSTNUM.BOARDORDER[new_pos],new_pos))    
    
    return

def isJumpSquare(spaceship):
    if (spaceship.current == -1):
        return False
    if (spaceship.color == 'purple'):
        if (spaceship.current % 4 == 0) and (spaceship.current != CONSTNUM.PURPLEEND):
            return True
        else:
            return False
    elif (spaceship.color == 'blue'):
        if ((spaceship.current-1) % 4 == 0) and (spaceship.current != CONSTNUM.BLUEEND):
            return True
        else:
            return False
    elif (spaceship.color == 'red'):
        if ((spaceship.current-2) % 4 == 0) and (spaceship.current != CONSTNUM.REDEND):
            return True
        else:
            return False
    elif (spaceship.color == 'teal'):
        if ((spaceship.current-3) % 4 == 0) and (spaceship.current != CONSTNUM.TEALEND):
            return True
        else:
            return False
    else:
        return False
    
def getJumpSquare(spaceship):
    new_pos = (spaceship.current+4) % CONSTNUM.BOARDMODULO
    return (CONSTNUM.BOARDORDER[new_pos],new_pos)


def validSquaresForDice(player, roll):
    spaceships = player.spaceships
    movable_spaceships = []
    if (roll == 6):
        for spaceship in spaceships:
            if spaceship.isInEnding != True:
                movable_spaceships.append(spaceship)
    else:
        for spaceship in spaceships:
            if (spaceship.isInBase == False):
                if ((spaceship.isInEnding == True) and ((spaceship.current + roll) >=6)):
                    pass
                else: 
                    movable_spaceships.append(spaceship)
    
    for spaceship in movable_spaceships:
        spaceship.movable = True
        spaceship.movable_squares = []
        getNewPos(spaceship, roll, player)
        
    if len(movable_spaceships) == 0:
        return False
    else:
        return True


    