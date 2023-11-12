import pygame
import cv2
import numpy
from constants import strings as CONSTSTR
from constants import numerics as CONSTNUM
from constants.globalvars import BOARD_POS
from modules.helpers.squarehelpers import getSquareUnderMouse, isLongTile
from menus import button as button_module, dicebutton as dicebutton_module

pygame.init()

headerFont = pygame.font.Font("menus/fonts/orbitron/static/Orbitron-Black.ttf", 86)
subHeaderFont = pygame.font.Font("menus/fonts/robotocondensed/RobotoCondensed-Regular.ttf", 64)
paragraphFont = pygame.font.Font("menus/fonts/opensans/Open_Sans/static/OpenSans_Condensed-Regular.ttf", 32)
diceFont = pygame.font.Font("menus/fonts/orbitron/static/Orbitron-Black.ttf", 32)
nameFont = pygame.font.Font("menus/fonts/opensans/Open_Sans/static/OpenSans_Condensed-Regular.ttf", 20)
textColor = (255, 255, 255)

def drawText(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return

def drawBackground(menu, imgPath):
    bg = pygame.image.load(imgPath).convert_alpha()
    menu.blit(bg, (0,0))

def drawButton(menu, imgPath, xRatio, yRatio, scale):
    img = pygame.image.load(imgPath).convert_alpha()
    imgDim = img.get_rect()
    xPos = (menu.get_width() - imgDim.width) * xRatio
    yPos = (menu.get_height() - imgDim.height) * yRatio
    button = button_module.Button(xPos, yPos, img, scale)
    button.draw(menu)
    return button

def draw_rounded_rect(surface, color, rect, border_radius):
    pygame.draw.rect(surface, color, (rect.x + border_radius, rect.y, rect.width - 2 * border_radius, rect.height))
    pygame.draw.rect(surface, color, (rect.x, rect.y + border_radius, rect.width, rect.height - 2 * border_radius))
    pygame.draw.circle(surface, color, (rect.x + border_radius, rect.y + border_radius), border_radius)
    pygame.draw.circle(surface, color, (rect.x + rect.width - border_radius, rect.y + border_radius), border_radius)
    pygame.draw.circle(surface, color, (rect.x + border_radius, rect.y + rect.height - border_radius), border_radius)
    pygame.draw.circle(surface, color, (rect.x + rect.width - border_radius, rect.y + rect.height - border_radius), border_radius)

def draw_translucent_rectangle(surface, x, y, width, height, color, alpha):
    rectangle = pygame.Surface((width, height), pygame.SRCALPHA)
    rectangle.fill((color[0], color[1], color[2], alpha))
    surface.blit(rectangle, (x, y))

def create_name_input(menu, xRatio, yRatio, num):
    boxWidth = 500
    boxHeight = 48
    square_size = 40
    purple = (125,98,140)
    blue = (64,94,127)
    red = (134,87,99)
    teal = (76,124,140)
    if num == 1:    # player 1
        drawText("Player 1: ", paragraphFont, textColor, menu, menu.get_width() * 0.175, menu.get_height() * 0.36)
        box = pygame.Rect(menu.get_width()*xRatio, menu.get_height()*yRatio, boxWidth, boxHeight)
        purple_square_rect = pygame.Rect(menu.get_width()*0.72, menu.get_height()*0.375, square_size, square_size)
        pygame.draw.rect(menu, purple, purple_square_rect)
        pygame.draw.rect(menu, textColor, purple_square_rect, 2)
    elif num == 2:  # player 2
        drawText("Player 2: ", paragraphFont, textColor, menu, menu.get_width() * 0.175, menu.get_height() * 0.46)
        box = pygame.Rect(menu.get_width()*xRatio, menu.get_height()*yRatio, boxWidth, boxHeight)
        blue_square_rect = pygame.Rect(menu.get_width()*0.72, menu.get_height()*0.475, square_size, square_size)
        pygame.draw.rect(menu, blue, blue_square_rect)
        pygame.draw.rect(menu, textColor, blue_square_rect, 2)
    elif num == 3:  # player 3
        drawText("Player 3: ", paragraphFont, textColor, menu, menu.get_width() * 0.175, menu.get_height() * 0.56)
        red_square_rect = pygame.Rect(menu.get_width()*0.72, menu.get_height()*0.575, square_size, square_size)
        box = pygame.Rect(menu.get_width()*xRatio, menu.get_height()*yRatio, boxWidth, boxHeight)
        pygame.draw.rect(menu, red, red_square_rect)
        pygame.draw.rect(menu, textColor, red_square_rect, 2)
    elif num == 4:  # player 4
        drawText("Player 4: ", paragraphFont, textColor, menu, menu.get_width() * 0.175, menu.get_height() * 0.66)
        teal_square_rect = pygame.Rect(menu.get_width()*0.72, menu.get_height()*0.675, square_size, square_size)
        box = pygame.Rect(menu.get_width()*xRatio, menu.get_height()*yRatio, boxWidth, boxHeight)
        pygame.draw.rect(menu, teal, teal_square_rect)
        pygame.draw.rect(menu, textColor, teal_square_rect, 2)
    return box

def create_player_num_input(menu, xRatio, yRatio, choice):
    width = 220
    height = 48
    if choice == 1: # player number
        drawText("Num of Players: ", paragraphFont, textColor, menu, menu.get_width() * 0.175, menu.get_height() * 0.16)
        box = pygame.Rect(menu.get_width()*(xRatio+0.05), menu.get_height()*yRatio, width, height)
    if choice == 2: # AI number
        drawText("Num of AIs: ", paragraphFont, textColor, menu, menu.get_width() * 0.175, menu.get_height() * 0.26)
        box = pygame.Rect(menu.get_width()*(xRatio+0.05), menu.get_height()*yRatio, width, height)
    return box

def draw_input_box(screen, rect, color, text=""):
    draw_rounded_rect(screen, color, rect, 12)
    text_surface = paragraphFont.render(text, True, (0,0,0))
    screen.blit(text_surface, (rect.x+5, rect.y-5))

def draw_2layer_container(menu, imgPath):
    drawBackground(menu, imgPath)
    rect_width, rect_height = 960, 675
    x = menu.get_width()*0.11
    y = menu.get_height()*0.05
    layer1 = pygame.Rect(x, y, rect_width, rect_height)
    draw_rounded_rect(menu, (211, 211, 211), layer1, 50)
    rect_width, rect_height = 880, 605
    x = menu.get_width()*0.14
    y = menu.get_height()*0.1
    layer2 = pygame.Rect(x, y, rect_width, rect_height)
    draw_rounded_rect(menu, (128, 128, 128), layer2, 50) 