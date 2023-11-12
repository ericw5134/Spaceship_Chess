import pygame
from modules.helpers.drawhelpers import drawCircle
from constants import numerics as CONSTNUM
class BaseBoardSquare():
    def __init__(self, coord, color) -> None:
        self.x = coord[1]
        self.y = coord[0]
        self.color = color

    def draw(self,board_surf):
        circ = ((self.x *CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2), ( self.y *CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2))
        rect = pygame.Rect((self.x*CONSTNUM.TILESIZE)-CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)-CONSTNUM.OFFSET,CONSTNUM.TILESIZE+2*CONSTNUM.OFFSET,CONSTNUM.TILESIZE+2*CONSTNUM.OFFSET)
        pygame.draw.rect(board_surf, self.color, rect)
        drawCircle(board_surf, (255, 255, 255), circ, 8, 3)