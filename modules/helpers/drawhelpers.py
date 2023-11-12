import pygame
import cv2
import numpy
from constants import strings as CONSTSTR
from constants import numerics as CONSTNUM
from constants.globalvars import BOARD_POS
from modules.helpers.squarehelpers import getSquareUnderMouse, isLongTile

def loadPieceImage(color):
    if color == "purple":
            return pygame.image.load(CONSTSTR.PURPLE_PLAYER_SPRITE_LOCATION).convert_alpha()
    elif color == "blue":
        return pygame.image.load(CONSTSTR.BLUE_PLAYER_SPRITE_LOCATION).convert_alpha()
    elif color == "red":
        return pygame.image.load(CONSTSTR.RED_PLAYER_SPRITE_LOCATION).convert_alpha()
    elif color == "teal":
        return pygame.image.load(CONSTSTR.TEAL_PLAYER_SPRITE_LOCATION).convert_alpha()
    else:
        return pygame.image.load(CONSTSTR.TRANSPARENT_SPRITE_LOCATION).convert_alpha()

def drawCircle(surf, color, center, radius, width):
    circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
    circle_image = cv2.circle(circle_image, (radius+2, radius+2), radius-width//2, (*color, 255), width, lineType=cv2.LINE_AA)  
    circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center = center))

def drawDragCircle(x,y,color, surface):
    if (isLongTile(x,y)):
        if (((y==0 or y==15) and (x>=4 and x<=12))):
            circ = ((BOARD_POS[0] + x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2), ((BOARD_POS[1] + y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE)))
            drawCircle(surface, color, circ, 18, 2)
        elif (((x==0 or x==15) and (y>=4 and y<=12))):
            circ = ((BOARD_POS[0] + x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE), (BOARD_POS[1] + y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2))
            drawCircle(surface, color, circ, 18, 2)
    else:
        circ = ((BOARD_POS[0] + x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2), (BOARD_POS[1] + y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2))
        drawCircle(surface, color, circ, 18, 2)

def drawDragPos(screen, board, selected_piece):
    if selected_piece:
        _, x, y = getSquareUnderMouse(board)
        if x != None:
            for square in selected_piece[0].movable_squares:
                if square[0][0] == y and square[0][1] == x:
                    drawDragCircle(x, y, (0, 255, 0), screen)
        color = selected_piece[0].color
        s1 = loadPieceImage(color)
        s2 = loadPieceImage("transparent")
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
        screen.blit(s1, s1.get_rect(center=pos))
        if (isLongTile(selected_piece[1],selected_piece[2])):
            if (((selected_piece[2]==0 or selected_piece[2]==15) and (selected_piece[1]>=4 and selected_piece[1]<=12))):
                selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * CONSTNUM.TILESIZE+1, BOARD_POS[1] + selected_piece[2] * CONSTNUM.TILESIZE + 1, CONSTNUM.TILESIZE, 2*CONSTNUM.TILESIZE)
            else:
                selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * CONSTNUM.TILESIZE+1, BOARD_POS[1] + selected_piece[2] * CONSTNUM.TILESIZE + 1, 2*CONSTNUM.TILESIZE, CONSTNUM.TILESIZE)
        else:
            selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * CONSTNUM.TILESIZE+1, BOARD_POS[1] + selected_piece[2] * CONSTNUM.TILESIZE + 1, CONSTNUM.TILESIZE, CONSTNUM.TILESIZE)
        pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return (x, y)
    
def drawSelector(screen, spaceship, x, y):
    #spaceship.movable = True # Chris added for testing
    if spaceship != None and spaceship.movable == True:

        drawDragCircle(x, y, (255, 69, 0), screen)

def drawHighlightPossiblePieces(screen, player):
    for spaceship in player.spaceships:
        if (spaceship.movable == True):
            y, x = spaceship.location
            drawDragCircle(x, y, (0, 255, 0), screen)

def drawMovableSquares(screen, spaceship):
    for square in spaceship.movable_squares:
        drawDragCircle(square[0][1], square[0][0], (255, 69, 0), screen)

       
def drawPieces(screen, board, selected_piece):
    sx, sy = None, None
    if selected_piece:
        piece, sx, sy = selected_piece

    for y in range(CONSTNUM.BOARDSIZE):
        for x in range(CONSTNUM.BOARDSIZE): 
            pieces = board[y][x]
            if pieces:
                for piece in pieces:
                    selected = x == sx and y == sy
                    
                    color = piece.color
                    #color = 'red' # Chris: I hardcoded to get it working. This is commented out for your testing.

                    s1 = loadPieceImage("transparent") if selected else loadPieceImage(color)
                    s2 = loadPieceImage("transparent")
                    
                    if (isLongTile(x,y)):
                        if (((y==0 or y==15) and (x>=4 and x<=12))):
                            pos = pygame.Rect(BOARD_POS[0] + x * CONSTNUM.TILESIZE+1, BOARD_POS[1] + y * CONSTNUM.TILESIZE + 1, CONSTNUM.TILESIZE, 2*CONSTNUM.TILESIZE)
                        else:
                            pos = pygame.Rect(BOARD_POS[0] + x * CONSTNUM.TILESIZE+1, BOARD_POS[1] + (y) * CONSTNUM.TILESIZE + 1, 2*CONSTNUM.TILESIZE, CONSTNUM.TILESIZE)
                        screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                        screen.blit(s1, s1.get_rect(center=pos.center))
                    else:
                        pos = pygame.Rect(BOARD_POS[0] + x * CONSTNUM.TILESIZE+1, BOARD_POS[1] + y * CONSTNUM.TILESIZE + 1, CONSTNUM.TILESIZE, CONSTNUM.TILESIZE)
                        screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                        screen.blit(s1, s1.get_rect(center=pos.center))
