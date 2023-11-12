import pygame
from modules.helpers.drawhelpers import drawCircle
from constants import numerics as CONSTNUM
class BoardSquare():
    def __init__(self, coord, color) -> None:
        self.x = coord[1]
        self.y = coord[0]
        self.color = color

    def draw(self,board_surf):
        if (((self.y==0 or self.y==15) and (self.x>4 and self.x<12))):
            rect = pygame.Rect((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, CONSTNUM.BOXSIZE, CONSTNUM.BOXSIZE*2+2*CONSTNUM.OFFSET)
            pygame.draw.rect(board_surf, self.color, rect)
            circ = (( self.x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2), ((self.y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE)))
            drawCircle(board_surf, (255, 255, 255), circ, 8, 3)
        elif ((self.x==0 or self.x==15) and (self.y>4 and self.y<12)):
            rect = pygame.Rect((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, CONSTNUM.BOXSIZE*2+2*CONSTNUM.OFFSET, CONSTNUM.BOXSIZE)
            pygame.draw.rect(board_surf, self.color, rect)
            circ = (( self.x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE), ( self.y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2))
            drawCircle(board_surf, (255, 255, 255), circ, 8, 3)
        else:
            circ = ((self.x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2), ( self.y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2))
            rect = pygame.Rect((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, CONSTNUM.BOXSIZE, CONSTNUM.BOXSIZE)
            pygame.draw.rect(board_surf, self.color, rect)
            drawCircle(board_surf, (255, 255, 255), circ, 8, 3)