import pygame
import pygame.gfxdraw
from modules.helpers.drawhelpers import drawCircle
from constants import numerics as CONSTNUM

class EndBoardSqure():
    def __init__(self, coord, color, team) -> None:
        self.x = coord[1]
        self.y = coord[0]
        self.color = color
        self.team = team
    
    def draw(self,board_surf):
        if (self.team == 'purple'):
            triangle = ((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+(CONSTNUM.BOXSIZE//2))
        elif (self.team == 'blue'):
            triangle = ((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+(CONSTNUM.BOXSIZE//2), (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET)
        elif (self.team == 'red'):
            triangle = ((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+(CONSTNUM.BOXSIZE//2))
        elif (self.team == 'teal'):
            triangle = ((self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE, (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET,(self.x*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+(CONSTNUM.BOXSIZE//2), (self.y*CONSTNUM.TILESIZE)+CONSTNUM.OFFSET+CONSTNUM.BOXSIZE)

        circ = ((self.x * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2), ( self.y * CONSTNUM.TILESIZE) + (CONSTNUM.TILESIZE//2))
        pygame.gfxdraw.aatrigon(board_surf,triangle[0], triangle[1], triangle[2], triangle[3], triangle[4], triangle[5],self.color)
        pygame.gfxdraw.filled_trigon(board_surf,triangle[0], triangle[1], triangle[2], triangle[3], triangle[4], triangle[5],self.color)
        drawCircle(board_surf, (255, 255, 255), circ, 8, 3)