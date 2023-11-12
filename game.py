import pygame, sys
import pygame.font
import math
from pygame.locals import *
from menus import button, escmenu
from menus import dicebutton
from constants import strings as CONSTSTR
from constants import numerics as CONSTNUM
import time
from modules.interface import interface
from modules.logic import dice
from modules.logic import gamesetup as gamesetup
from modules.player import humanplayer, aiplayer, spaceship, player
from constants.globalvars import BOARD_POS
from modules.helpers.drawhelpers import drawDragPos, drawPieces, drawSelector, drawHighlightPossiblePieces, drawMovableSquares
from modules.helpers.squarehelpers import isValidSquare, getSquareUnderMouse, validSquaresForDice,isEndingSquare, isLastSquare, isJumpSquare, getJumpSquare
from modules.helpers.boardhelpers import createBoard, createBoardSurf, createBoardLoad
from modules.helpers import drawstyle
import pandas as pd
import numpy as np
import os.path

# game screen setup
mainClock = pygame.time.Clock()
FPS = 60
pygame.init()
gameWidth = 1280
gameHeight = 720
screen = pygame.display.set_mode((gameWidth, gameHeight),0,32)
pygame.display.set_caption("Spaceship Chess")

# fonts
headerFont = pygame.font.Font("menus/fonts/orbitron/static/Orbitron-Black.ttf", 86)
subHeaderFont = pygame.font.Font("menus/fonts/robotocondensed/RobotoCondensed-Regular.ttf", 64)
paragraphFont = pygame.font.Font("menus/fonts/opensans/Open_Sans/static/OpenSans_Condensed-Regular.ttf", 32)
diceFont = pygame.font.Font("menus/fonts/orbitron/static/Orbitron-Black.ttf", 32)
nameFont = pygame.font.Font("menus/fonts/opensans/Open_Sans/static/OpenSans_Condensed-Regular.ttf", 20)
textColor = (255, 255, 255)
easterEgg_textColor = (int(127 + 127 * (pygame.time.get_ticks() % 2000 / 1000)), 
                      int(127 + 127 * (pygame.time.get_ticks() % 3000 / 1000)), 
                      int(127 + 127 * (pygame.time.get_ticks() % 4000 / 1000)))

# load background image 
background = pygame.image.load("menus/images/background.png").convert_alpha()

# music / sounds
music = pygame.mixer.music.load('assets/ogg/HOME-Resonance.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.20)
DICE_SOUND = pygame.mixer.Sound('assets/wav/UI.wav')
DICE_SOUND.set_volume(0.02)
clickSound = pygame.mixer.Sound('assets/wav/button_click.wav')
clickSound.set_volume(0.1)
easterEggSound = pygame.mixer.Sound('assets/wav/button_click_easterEgg.wav')
easterEggSound.set_volume(0.1)
shipSound = pygame.mixer.Sound('assets/wav/ship.wav')
shipSound.set_volume(0.3)

# asserts to be loaded
# load all the dice images, once the most recently drawn will be visible
diceImg1 = pygame.image.load("menus/images/dices/1.png").convert_alpha()
diceImg2 = pygame.image.load("menus/images/dices/2.png").convert_alpha()
diceImg3 = pygame.image.load("menus/images/dices/3.png").convert_alpha()
diceImg4 = pygame.image.load("menus/images/dices/4.png").convert_alpha()
diceImg5 = pygame.image.load("menus/images/dices/5.png").convert_alpha()
diceImg6 = pygame.image.load("menus/images/dices/6.png").convert_alpha()

# load the sprites
BLUE_SPRITE = pygame.image.load(CONSTSTR.BLUE_PLAYER_SPRITE_LOCATION).convert_alpha()
TEAL_SPRITE = pygame.image.load(CONSTSTR.TEAL_PLAYER_SPRITE_LOCATION).convert_alpha()
RED_SPRITE = pygame.image.load(CONSTSTR.RED_PLAYER_SPRITE_LOCATION).convert_alpha()
PURPLE_SPRITE = pygame.image.load(CONSTSTR.PURPLE_PLAYER_SPRITE_LOCATION).convert_alpha()


# Chris: made a global variable 'reload'
reload = False

#Instantiate the bridge structure
Interface = interface.Interface()

# each screen has their own setup
def mainMenu(menu):

    drawstyle.drawBackground(menu, "menus/images/background.png")
    mainClock.tick(60)
    xRatio = 0.845
    yRatio = 0.125
    scale = 0.35
    logoEasterEgg = drawstyle.drawButton(menu, "menus/images/logo.png", xRatio, yRatio, scale)
    logoEasterEggClicked = 0
    drawstyle.drawText("Spaceship      Chess", headerFont, textColor, menu, menu.get_width() * 0.1, menu.get_height() * 0.1)

    xRatio = 0.5 
    yRatio = 0.425
    scale = 1
    newGameButton = drawstyle.drawButton(menu, "menus/images/button_newgame.png", xRatio, yRatio, scale)

    yRatio = 0.675
    loadSaveButton = drawstyle.drawButton(menu, "menus/images/button_loadgame.png", xRatio, yRatio, scale)
    
    xRatio = 0.54
    yRatio = 0.95
    scale = 0.7
    exitButton = drawstyle.drawButton(menu, "menus/images/button_exit.png", xRatio, yRatio, scale)

    xRatio = 0.975
    yRatio = 0.975
    scale = 0.8
    achieveButton = drawstyle.drawButton(menu, "assets/gfx/Achievement_button.png", xRatio, yRatio, scale)
    
    running = True
    while running:

        # .draw() checks if the button is pressed as well, 
        # returns true if clicked
        if newGameButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            print("pressed newgame")
            running = False
            gameSettingsMenu(menu)

        if logoEasterEgg.draw(menu):
            pygame.mixer.Sound.play(easterEggSound)
            print("triggered")
            logoEasterEggClicked += 1
            print(logoEasterEggClicked)
        
        if logoEasterEggClicked >= 5:
            xRatio = 0.62
            yRatio = 0.071
            scale = 0.675
            logoEasterEgg = drawstyle.drawButton(menu, "assets/gfx/Rainbow_Logo.png", xRatio, yRatio, scale)

        if achieveButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            print("pressed achievement")
            running = False
            achieveMenu(menu)
        
        if loadSaveButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            pygame.mixer.music.fadeout(2)
            pygame.mixer.music.load('assets/ogg/Neon.Deflector - Star Dreamer.ogg')
            pygame.mixer.music.play(-1, 0, 2)
            print("pressed loadsave")            
            if os.path.exists('./load_game_board.csv'):
                running = True
                board = pd.read_csv('load_game_board.csv',index_col=False)
                stats = pd.read_csv('load_game_stats.csv',index_col=False)
                names = stats['player_name']
                scores = stats['score']
                board = board.replace(np.nan,None)
                board = board.to_numpy()
                spaceship, x, y = getSquareUnderMouse(board)
                reload = True
                gameMenuLoad(menu,names,scores,board)
                reload = False # finished loading the board
            else:
                print("no save file")
                running = False
                gameSettingsMenu(menu)
        
        if exitButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            pygame.quit()
            sys.exit()

        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        mainClock.tick(60)

def achieveMenu(menu):

    ROLLED_6 = False
    LAUNCH_FIRST_PLANE = False
    SPECIAL_TILE = False

    if os.path.exists('./achievements.csv'):
        achievementStatus = pd.read_csv('achievements.csv',index_col=False)
        status_col = status_column = achievementStatus['0']
        ROLLED_6 = status_col[0]
        LAUNCH_FIRST_PLANE = status_col[1]
        SPECIAL_TILE = status_col[2]
    else:
        pass

    mainClock.tick(60)
    menu.fill((0,0,0))
    drawstyle.draw_2layer_container(menu, "menus/images/background.png")

    xRatio = 0.35
    yRatio = 0.1
    drawstyle.drawText("Achievements", subHeaderFont, textColor, menu, menu.get_width()*xRatio, menu.get_height()*yRatio)
    
    xRatio = 0.825
    yRatio = 0.91
    scale = 0.7
    returnButton = drawstyle.drawButton(menu, "menus/images/button_return.png", xRatio, yRatio, scale)

    xRatio = 0.2
    yRatio = 0.3
    scale = 1
    luckyAchieve = None
    if ROLLED_6:
        luckyAchieve = drawstyle.drawButton(menu, "assets/gfx/Lucky_Roll_Gold.png", xRatio, yRatio, scale)
    else: 
        luckyAchieve = drawstyle.drawButton(menu, "assets/gfx/Lucky_Roll.png", xRatio, yRatio, scale)
    drawstyle.drawText("LUCKY ROLL", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio-0.05))
    drawstyle.drawText("Roll your first '6' ", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio+0.05))
    drawstyle.drawText("in a game", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio+0.1))
    
    xRatio = 0.4
    yRatio = 0.595
    firstFlightAchieve = None
    if LAUNCH_FIRST_PLANE:
        firstFlightAchieve = drawstyle.drawButton(menu, "assets/gfx/First_Flight_Gold.png", xRatio, yRatio, scale)
    else: 
        firstFlightAchieve = drawstyle.drawButton(menu, "assets/gfx/First_Flight.png", xRatio, yRatio, scale)
    drawstyle.drawText("FIRST FLIGHT", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio-0.15))
    drawstyle.drawText("Launch a plane from base", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio-0.05))
    drawstyle.drawText("for the first time", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio))
    
    xRatio = 0.2
    yRatio = 0.85
    ShortcutAchieve = None
    if SPECIAL_TILE:
        firstFlightAchieve = drawstyle.drawButton(menu, "assets/gfx/ShortCut_Master_Gold.png", xRatio, yRatio, scale)
    else:
        firstFlightAchieve = drawstyle.drawButton(menu, "assets/gfx/ShortCut_Master.png", xRatio, yRatio, scale)
    drawstyle.drawText("SHORTCUT MASTER", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio-0.15))
    drawstyle.drawText("Use a special tile to", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio-0.05))
    drawstyle.drawText("warp across the board", paragraphFont, textColor, menu, menu.get_width()*(xRatio+0.1), menu.get_height()*(yRatio))

    running = True
    while running:
        if returnButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            running = False
            mainMenu(menu)
        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        mainClock.tick(60)

def escMenu(menu, names):
    
    # clear page
    mainClock.tick(60)
    menu.fill((0,0,0))
    drawstyle.drawBackground(menu, "menus/images/background.png")
    xRatio = 0.5
    yRatio = 0.3
    scale = 1
    resumeButton = drawstyle.drawButton(menu, "menus/images/button_return.png", xRatio, yRatio, scale)
    yRatio = 0.5
    optionsButton = drawstyle.drawButton(menu, "menus/images/button_settings.png", xRatio, yRatio, scale)
    yRatio = 0.7
    quitButton = drawstyle.drawButton(menu, "menus/images/button_exit.png", xRatio, yRatio, scale)
    
    running = True
    while running:

        if resumeButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            running = False
            gameMenu(menu, names)

        if optionsButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            settingsMenu(menu, names)

        if quitButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            pygame.quit()
            sys.exit()

        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False 
                    gameMenu(menu, names)

        pygame.display.update()
        mainClock.tick(60)

def settingsMenu(menu, names):
    mainClock.tick(60)
    menu.fill((0,0,0))
    drawstyle.drawBackground(menu, "menus/images/background.png")
    xRatio = 0.845
    yRatio = 0.125
    scale = 0.35
    logoEasterEgg = drawstyle.drawButton(menu, "menus/images/logo.png", xRatio, yRatio, scale)
    drawstyle.drawText("Spaceship      Chess", headerFont, textColor, menu, menu.get_width() * 0.1, menu.get_height() * 0.1)
    xRatio, yRatio = 0.225, 0.45
    drawstyle.drawText("There's nothing to see here", subHeaderFont, textColor, menu, menu.get_width()*xRatio, menu.get_height()*yRatio)
    xRatio = 0.5
    yRatio = 0.9
    scale = 1
    returnButton = drawstyle.drawButton(menu, "menus/images/button_return.png", xRatio, yRatio, scale)
    running = True
    while running:
        if returnButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            gameMenu(menu, names)        
        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        mainClock.tick(60)    

def gameSettingsMenu(menu):

    mainClock.tick(60)
    menu.fill((0,0,0))
    drawstyle.draw_2layer_container(menu, "menus/images/background.png")
    
    Interface.printDictionary()
    GameSetup = gamesetup.GameSetup(4, 3, 1)
    Interface.updatePlayerInformation(GameSetup.get_player_info())

    # user input
    names = ['', '', '', '']
    xRatio = 0.3
    yRatio = 0.37
    currPlayer = 1
    p1Box = drawstyle.create_name_input(menu, xRatio, yRatio, currPlayer)
    yRatio = 0.47
    currPlayer = 2
    p2Box = drawstyle.create_name_input(menu, xRatio, yRatio, currPlayer)
    yRatio = 0.57
    currPlayer = 3
    p3Box = drawstyle.create_name_input(menu, xRatio, yRatio, currPlayer)
    yRatio = 0.67
    currPlayer = 4
    p4Box = drawstyle.create_name_input(menu, xRatio, yRatio, currPlayer)
    input_boxes = [p1Box, p2Box, p3Box, p4Box]
    active_input_box = None

    # buttons & logo
    xRatio = 0.35
    yRatio = 0.9
    scale = 1
    returnButton = drawstyle.drawButton(menu, "menus/images/button_return.png", xRatio, yRatio, scale)
    xRatio = 0.65
    startGameButton = drawstyle.drawButton(menu, "menus/images/button_startgame.png", xRatio, yRatio, scale)
    xRatio = 0.175
    yRatio = 0.16
    drawstyle.drawText("Hello pilots, Are you ready for an advanture?", paragraphFont, textColor, menu, menu.get_width()*xRatio, menu.get_height()*yRatio)
    yRatio = 0.26
    drawstyle.drawText("But first, what are your names?", paragraphFont, textColor, menu, menu.get_width()*xRatio, menu.get_height()*yRatio)
    xRatio = 1.125
    yRatio = 0.275
    scale = 0.375
    logo = drawstyle.drawButton(menu, "menus/images/logo.png", xRatio, yRatio, scale)

    running = True
    while running:
        if returnButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            running = False
            mainMenu(menu)
        if startGameButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            print(names)
            pygame.mixer.music.fadeout(2)
            pygame.mixer.music.load('assets/ogg/Neon.Deflector - Star Dreamer.ogg')
            pygame.mixer.music.play(-1, 0, 2)
            running = False
            gameMenu(menu, names)
        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_input_box = box
                        break
                else:
                    active_input_box = None
            elif event.type == pygame.KEYDOWN:
                if active_input_box:
                    if event.key == pygame.K_RETURN:
                        active_input_box = None
                    elif event.key == pygame.K_BACKSPACE:
                        names[input_boxes.index(active_input_box)] = names[input_boxes.index(active_input_box)][:-1]
                    else:
                        names[input_boxes.index(active_input_box)] += event.unicode

        for box, text in zip(input_boxes, names):
            drawstyle.draw_input_box(menu, box, (255,255,255), text)

        pygame.display.flip()
        mainClock.tick(60)


def gameMenu(menu, names):
    # Draw Background
    menu.fill((0,0,0))
    menu.blit(background, (0,0))

    xRatio, yRatio, scale = 0.975, 0.975, 1
    saveButton = drawstyle.drawButton(menu,"menus/images/icon_saves.png", xRatio, yRatio, scale)

    # checking if there are empty names
    for i in range(4):
        if names[i] == '':
            names[i] = CONSTSTR.DEFAULT_PLAYER_NAMES[i]

    diceDim = diceImg1.get_rect()
    diceX = (menu.get_width() - diceDim.width) * 0.98
    diceY = (menu.get_height() - diceDim.height) * 0.25
    diceButton = dicebutton.DiceButton(diceX, diceY, diceImg1, 0.80)
    # Import the images into a dictionary
    diceButton.assign_image(1,diceImg1)
    diceButton.assign_image(2, diceImg2)
    diceButton.assign_image(3, diceImg3)
    diceButton.assign_image(4, diceImg4)
    diceButton.assign_image(5, diceImg5)
    diceButton.assign_image(6, diceImg6)
    # Then render the images so that they don't have to be recreated unless resize
    diceButton.render_images()

    Dice = dice.Dice(6, 150, 10)

    running = True
    selected_piece = None
    drop_pos = None
    turn = 0
    dice_rolled = False
    ROLLED_6 = False
    LAUNCH_FIRST_PLANE = False
    SPECIAL_TILE = False

    # Build players
    purple_player = player.Player(0,'purple')
    blue_player = player.Player(1,'blue')
    red_player = player.Player(2,'red')
    teal_player = player.Player(3,'teal')
    players = [purple_player, blue_player, red_player, teal_player]

    # Build Board
    board = createBoard(players)
    board_surf = createBoardSurf()    
    boardX = (gameWidth - 726) * 0.5
    boardY = (gameHeight- 726) * 0.2
    BOARD_POS[0] = boardX
    BOARD_POS[1] = boardY  

    scores = [0,0,0,0]

    while running:

        diceButton.draw(menu) 
        screen.blit(background, (0,0))

        # scoreboard
        rect_width, rect_height = 213, 386
        x = menu.get_width()*(29/1280)
        y = menu.get_height()*(178/720)
        layer1 = pygame.Rect(x, y, rect_width, rect_height)
        drawstyle.draw_translucent_rectangle(menu, x, y, rect_width, rect_height,(0,0,0), 64)
        drawstyle.drawText(CONSTSTR.CONSTANT_SCOREBOARD, paragraphFont, textColor, menu, 35, 90)
        drawstyle.drawText(names[0]+": "+str(scores[0]), paragraphFont, textColor, menu, 50, 190)
        drawstyle.drawText(names[1]+": "+str(scores[1]), paragraphFont, textColor, menu, 50, 290)
        drawstyle.drawText(names[2]+": "+str(scores[2]), paragraphFont, textColor, menu, 50, 390)
        drawstyle.drawText(names[3]+": "+str(scores[3]), paragraphFont, textColor, menu, 50, 490)

        drawstyle.drawText(names[0], nameFont, textColor, menu, menu.get_width()*0.655, menu.get_height()*0.88)
        drawstyle.drawText(names[1], nameFont, textColor, menu, menu.get_width()*0.29, menu.get_height()*0.88)
        drawstyle.drawText(names[2], nameFont, textColor, menu, menu.get_width()*0.29, menu.get_height()*0.06)
        drawstyle.drawText(names[3], nameFont, textColor, menu, menu.get_width()*0.655, menu.get_height()*0.06)

        # sample tip maybe but into tooltip later
        drawstyle.drawText('Tip: Press ESC to bring', paragraphFont, textColor, menu, menu.get_width() * 0.79, menu.get_height() * 0.60)
        drawstyle.drawText('up a menu to quit', paragraphFont, textColor, menu, menu.get_width() * 0.79, menu.get_height() * 0.65) 

        spaceships, x, y = getSquareUnderMouse(board)
        if spaceships!=None:
            spaceship = spaceships[0]
        else:
            spaceship = None
        #events = pygame.event.get()

        for e in pygame.event.get():

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                    escMenu(menu, names)

            if e.type == QUIT:
                # time to save the game for it to be loaded next time
                
                stats_df = pd.DataFrame({'player_name':names,'score':scores})
                board_df = pd.DataFrame(board)

                stats_df.to_csv('load_game_stats.csv',index=False) # csv for player stats
                board_df.to_csv('load_game_board.csv',index=False) # csv for saved board
                
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if spaceship != None and (CONSTSTR.AVAILABLE_COLORS[turn] == spaceship.color) and dice_rolled == True and spaceship.movable == True:
                    selected_piece = (spaceship, x, y)

            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    new_x, new_y = drop_pos
                    if (isValidSquare(new_x, new_y)):
                        LAUNCH_FIRST_PLANE = True
                        for square in selected_piece[0].movable_squares:
                            if square[0][0] == new_y and square[0][1] == new_x:
                                spaceship, old_x, old_y = selected_piece
                                old_square_spaceships = board[old_y][old_x]
                                if (isEndingSquare(new_x, new_y)):
                                    spaceship.isInEnding = True
                                if (len(old_square_spaceships)>1):
                                    new_list = list(filter(lambda old_spaceship: old_spaceship != spaceship, old_square_spaceships))
                                    board[old_y][old_x] = new_list
                                else:
                                    board[old_y][old_x] = None
                                if isLastSquare(new_x, new_y):
                                    board[new_y][new_x] = None
                                    scores[turn] += 50
                                    spaceship_list = list(filter(lambda old_spaceship: old_spaceship != spaceship, players[turn].spaceships))
                                    players[turn].spaceships = spaceship_list
                                    if (len(players[turn].spaceships)==0):
                                        winMenu(menu, names[turn])
                                    for spaceship in players[turn].spaceships:
                                        spaceship.movable = False
                                else:
                                    if board[new_y][new_x] != None:
                                        current_spaceships = board[new_y][new_x]
                                        if (current_spaceships[0].color == spaceship.color):
                                            current_spaceships.append(spaceship)
                                        else:
                                            for current_spaceship in current_spaceships:
                                                current_spaceship.location = current_spaceship.basePos
                                                board[current_spaceship.location[0]][current_spaceship.location[1]] = [current_spaceship]
                                                current_spaceship.isInBase = True
                                    else:
                                        board[new_y][new_x] = [spaceship]
                                    spaceship.location = (new_y,new_x)
                                    spaceship.isInBase = False
                                    spaceship.current = square[1]

                                    if (isJumpSquare(spaceship)):
                                        SPECIAL_TILE = True
                                        old_y, old_x = new_y, new_x
                                        pygame.mixer.Sound.play(shipSound)
                                        pygame.time.delay(500)
                                        board[old_y][old_x] = None
                                        (new_y, new_x), new_index = getJumpSquare(spaceship)
                                        if board[new_y][new_x] != None:
                                            current_spaceships = board[new_y][new_x]
                                            if (current_spaceships[0].color == spaceship.color):
                                                current_spaceships.append(spaceship)
                                            else:
                                                for current_spaceship in current_spaceships:
                                                    current_spaceship.location = current_spaceship.basePos
                                                    board[current_spaceship.location[0]][current_spaceship.location[1]] = [current_spaceship]
                                                    current_spaceship.isInBase = True
                                        else:
                                            board[new_y][new_x] = [spaceship]
                                        selected_piece[0].location = (new_y,new_x)
                                        selected_piece[0].current = new_index
                                    
                                    for spaceship in players[turn].spaceships:
                                        spaceship.movable = False
                                if (Dice.get_value()!=6):
                                    turn = (turn + 1) % 4
                                else:
                                    ROLLED_6 = True
                                dice_rolled = False
                selected_piece = None
                drop_pos = None
        boardBGWidth, boardBGHeight = 726, 726
        screen.blit(board_surf, BOARD_POS)
        x = BOARD_POS[0]
        y = BOARD_POS[1]
        layer1 = pygame.Rect(x,y,boardBGWidth, boardBGHeight)
        drawstyle.draw_translucent_rectangle(menu, x, y, boardBGWidth, boardBGHeight, (0,0,0), 32)
        drawPieces(screen, board, selected_piece)
        
        if Dice.is_rolling():
            index = Dice.roll()
            diceButton.update_image(menu, index)

        if diceButton.draw(menu):
           if diceButton.is_clicked() and dice_rolled == False:
                pygame.mixer.Sound.play(DICE_SOUND)
                Dice.throw_dice()
                dice_rolled = True
        
        if saveButton.draw(menu):
            # time to save the game for it to be loaded next time
            stats_df = pd.DataFrame({'player_name':names,'score':scores})
            achievements_df = pd.DataFrame([ROLLED_6, LAUNCH_FIRST_PLANE, SPECIAL_TILE])
            board_df = pd.DataFrame(board)
            #print(stats_df)
            print(board_df)
            stats_df.to_csv('load_game_stats.csv',index=False) # csv for player stats
            board_df.to_csv('load_game_board.csv',index=False) # csv for saved board
            achievements_df.to_csv('achievements.csv',index=False) # csv for achievements
            print(board[0][0])    

        if (not Dice.is_rolling()) and dice_rolled == False:
            drawstyle.drawText("GO", diceFont, textColor, menu, menu.get_width() * 0.87, menu.get_height() * 0.10)
            drawstyle.drawText(names[turn]+"'s", diceFont, textColor, menu, menu.get_width() * 0.825, menu.get_height() * 0.42) 
            drawstyle.drawText("turn", diceFont, textColor, menu, menu.get_width() * 0.86, menu.get_height() * 0.4875) 

        if (not Dice.is_rolling()) and dice_rolled == True:
            spaces = validSquaresForDice(players[turn], Dice.get_value())
            if spaces == False:
                drawstyle.drawText("NO MOVE", diceFont, textColor, menu, menu.get_width() * 0.825, menu.get_height() * 0.10)
                drawstyle.drawText("Roll: "+str(Dice.get_value()), diceFont, textColor, menu, menu.get_width() * 0.855, menu.get_height() * 0.42)
                turn = (turn + 1) % 4
                dice_rolled = False
                pygame.display.update()
                pygame.time.delay(1000) 
            else:
                drawstyle.drawText("MOVE", diceFont, textColor, menu, menu.get_width() * 0.85, menu.get_height() * 0.10)
                drawstyle.drawText("Roll: "+str(Dice.get_value()), diceFont, textColor, menu, menu.get_width() * 0.855, menu.get_height() * 0.42)
                if selected_piece == None:
                    drawHighlightPossiblePieces(screen, players[turn])
                else:
                    drawMovableSquares(screen, selected_piece[0])

        if selected_piece == None:
            drawSelector(screen, spaceship, x, y)
        
        drop_pos = drawDragPos(screen, board, selected_piece)    

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    escMenu(menu, names)

        pygame.display.update()
        mainClock.tick(60)
    
def gameMenuLoad(menu, names, scores, boardpass):
    # Draw Background
    menu.fill((0,0,0))
    menu.blit(background, (0,0))

    # checking if there are empty names
    for i in range(4):
        if names[i] == '':
            names[i] = CONSTSTR.DEFAULT_PLAYER_NAMES[i]

    diceDim = diceImg1.get_rect()
    diceX = (menu.get_width() - diceDim.width) * 0.98
    diceY = (menu.get_height() - diceDim.height) * 0.25
    diceButton = dicebutton.DiceButton(diceX, diceY, diceImg1, 0.80)
    xRatio, yRatio, scale = 0.975, 0.975, 1
    saveButton = drawstyle.drawButton(menu,"menus/images/icon_saves.png", xRatio, yRatio, scale)
    # Import the images into a dictionary
    diceButton.assign_image(1,diceImg1)
    diceButton.assign_image(2, diceImg2)
    diceButton.assign_image(3, diceImg3)
    diceButton.assign_image(4, diceImg4)
    diceButton.assign_image(5, diceImg5)
    diceButton.assign_image(6, diceImg6)
    # Then render the images so that they don't have to be recreated unless resize
    diceButton.render_images()

    Dice = dice.Dice(6, 150, 10)

    running = True
    selected_piece = None
    drop_pos = None
    turn = 0
    dice_rolled = False
    ROLLED_6 = False
    LAUNCH_FIRST_PLANE = False
    SPECIAL_TILE = False

    # Build players
    purple_player = player.Player(0,'purple')
    blue_player = player.Player(1,'blue')
    red_player = player.Player(2,'red')
    teal_player = player.Player(3,'teal')
    players = [purple_player, blue_player, red_player, teal_player]

    # Build Board
    # this board variable is passed as a parameter
    board = createBoardLoad(players,boardpass)
    
    board_surf = createBoardSurf()    
    boardX = (gameWidth - 726) * 0.5
    boardY = (gameHeight- 726) * 0.2
    BOARD_POS[0] = boardX
    BOARD_POS[1] = boardY  

    while running:
        ## Initialize the background/visual setup
        diceButton.draw(menu) 
        screen.blit(background, (0,0))

        # scoreboard
        rect_width, rect_height = 213, 386
        x = menu.get_width()*(29/1280)
        y = menu.get_height()*(178/720)
        layer1 = pygame.Rect(x, y, rect_width, rect_height)
        drawstyle.draw_translucent_rectangle(menu, x, y, rect_width, rect_height,(0,0,0), 64)
        drawstyle.drawText(CONSTSTR.CONSTANT_SCOREBOARD, paragraphFont, textColor, menu, 35, 90)
        
        #drawText("1"+": "+str(scores[0]), paragraphFont, textColor, menu, 50, 190)
        drawstyle.drawText(names[0]+": "+str(scores[0]), paragraphFont, textColor, menu, 50, 190)
        drawstyle.drawText(names[1]+": "+str(scores[1]), paragraphFont, textColor, menu, 50, 290)
        drawstyle.drawText(names[2]+": "+str(scores[2]), paragraphFont, textColor, menu, 50, 390)
        drawstyle.drawText(names[3]+": "+str(scores[3]), paragraphFont, textColor, menu, 50, 490)

        drawstyle.drawText(names[0], nameFont, textColor, menu, menu.get_width()*0.655, menu.get_height()*0.88)
        drawstyle.drawText(names[1], nameFont, textColor, menu, menu.get_width()*0.29, menu.get_height()*0.88)
        drawstyle.drawText(names[2], nameFont, textColor, menu, menu.get_width()*0.29, menu.get_height()*0.06)
        drawstyle.drawText(names[3], nameFont, textColor, menu, menu.get_width()*0.655, menu.get_height()*0.06)

        # sample tip maybe but into tooltip later
        drawstyle.drawText('Tip: Press ESC to bring', paragraphFont, textColor, menu, menu.get_width() * 0.79, menu.get_height() * 0.60)
        drawstyle.drawText('up the menu (or quit )', paragraphFont, textColor, menu, menu.get_width() * 0.79, menu.get_height() * 0.65) 

        spaceships, x, y = getSquareUnderMouse(board)
        if spaceships!=None:
            spaceship = spaceships[0]
        else:
            spaceship = None
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if spaceship != None and (CONSTSTR.AVAILABLE_COLORS[turn] == spaceship.color) and dice_rolled == True and spaceship.movable == True:
                    selected_piece = (spaceship, x, y)
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    new_x, new_y = drop_pos
                    if (isValidSquare(new_x, new_y)):
                        for square in selected_piece[0].movable_squares:
                            if square[0][0] == new_y and square[0][1] == new_x:
                                spaceship, old_x, old_y = selected_piece
                                old_square_spaceships = board[old_y][old_x]
                                if (isEndingSquare(new_x, new_y)):
                                    spaceship.isInEnding = True
                                if (len(old_square_spaceships)>1):
                                    new_list = list(filter(lambda old_spaceship: old_spaceship != spaceship, old_square_spaceships))
                                    board[old_y][old_x] = new_list
                                else:
                                    board[old_y][old_x] = None
                                if isLastSquare(new_x, new_y):
                                    board[new_y][new_x] = None
                                    scores[turn] += 50
                                    spaceship_list = list(filter(lambda old_spaceship: old_spaceship != spaceship, players[turn].spaceships))
                                    players[turn].spaceships = spaceship_list
                                    if (len(players[turn].spaceships)==0):
                                        print("You Win")
                                    for spaceship in players[turn].spaceships:
                                        spaceship.movable = False
                                else:
                                    if board[new_y][new_x] != None:
                                        current_spaceships = board[new_y][new_x]
                                        if (current_spaceships[0].color == spaceship.color):
                                            current_spaceships.append(spaceship)
                                        else:
                                            for current_spaceship in current_spaceships:
                                                current_spaceship.location = current_spaceship.basePos
                                                board[current_spaceship.location[0]][current_spaceship.location[1]] = [current_spaceship]
                                                current_spaceship.isInBase = True
                                    else:
                                        board[new_y][new_x] = [spaceship]
                                    spaceship.location = (new_y,new_x)
                                    spaceship.isInBase = False
                                    spaceship.current = square[1]

                                    if (isJumpSquare(spaceship)):
                                        old_y, old_x = new_y, new_x
                                        pygame.mixer.Sound.play(shipSound)
                                        pygame.time.delay(500)
                                        board[old_y][old_x] = None
                                        (new_y, new_x), new_index = getJumpSquare(spaceship)
                                        if board[new_y][new_x] != None:
                                            current_spaceships = board[new_y][new_x]
                                            if (current_spaceships[0].color == spaceship.color):
                                                current_spaceships.append(spaceship)
                                            else:
                                                for current_spaceship in current_spaceships:
                                                    current_spaceship.location = current_spaceship.basePos
                                                    board[current_spaceship.location[0]][current_spaceship.location[1]] = [current_spaceship]
                                                    current_spaceship.isInBase = True
                                        else:
                                            board[new_y][new_x] = [spaceship]
                                        selected_piece[0].location = (new_y,new_x)
                                        selected_piece[0].current = new_index
                                    
                                    for spaceship in players[turn].spaceships:
                                        spaceship.movable = False
                                if (Dice.get_value()!=6):
                                    turn = (turn + 1) % 4
                                dice_rolled = False
                selected_piece = None
                drop_pos = None
        boardBGWidth, boardBGHeight = 726, 726
        screen.blit(board_surf, BOARD_POS)
        x = BOARD_POS[0]
        y = BOARD_POS[1]
        layer1 = pygame.Rect(x,y,boardBGWidth, boardBGHeight)
        drawstyle.draw_translucent_rectangle(menu, x, y, boardBGWidth, boardBGHeight, (0,0,0), 32)
        drawPieces(screen, board, selected_piece)
        
        if Dice.is_rolling():
            index = Dice.roll()
            diceButton.update_image(menu, index)

        if diceButton.draw(menu):
            if diceButton.is_clicked() and dice_rolled == False:
                pygame.mixer.Sound.play(DICE_SOUND)
                Dice.throw_dice()
                dice_rolled = True
        if saveButton.draw(menu):
            # time to save the game for it to be loaded next time
            stats_df = pd.DataFrame({'player_name':names,'score':scores})
            achievements_df = pd.DataFrame([ROLLED_6, LAUNCH_FIRST_PLANE, SPECIAL_TILE])
            board_df = pd.DataFrame(board)
            #print(stats_df)
            print(board_df)
            stats_df.to_csv('load_game_stats.csv',index=False) # csv for player stats
            board_df.to_csv('load_game_board.csv',index=False) # csv for saved board
            achievements_df.to_csv('achievements.csv',index=False) # csv for achievements
            print(board[0][0])           

        if (not Dice.is_rolling()) and dice_rolled == False:
            drawstyle.drawText("GO", diceFont, textColor, menu, menu.get_width() * 0.87, menu.get_height() * 0.10)
            drawstyle.drawText(names[turn]+"'s", diceFont, textColor, menu, menu.get_width() * 0.825, menu.get_height() * 0.42) 
            drawstyle.drawText("turn", diceFont, textColor, menu, menu.get_width() * 0.86, menu.get_height() * 0.4875) 

        if (not Dice.is_rolling()) and dice_rolled == True:
            spaces = validSquaresForDice(players[turn], Dice.get_value())
            if spaces == False:
                drawstyle.drawText("NO MOVE", diceFont, textColor, menu, menu.get_width() * 0.825, menu.get_height() * 0.10)
                drawstyle.drawText("Roll: "+str(Dice.get_value()), diceFont, textColor, menu, menu.get_width() * 0.855, menu.get_height() * 0.42)
                turn = (turn + 1) % 4
                dice_rolled = False
                pygame.display.update()
                pygame.time.delay(1000) 
            else:
                drawstyle.drawText("MOVE", diceFont, textColor, menu, menu.get_width() * 0.85, menu.get_height() * 0.10)
                drawstyle.drawText("Roll: "+str(Dice.get_value()), diceFont, textColor, menu, menu.get_width() * 0.855, menu.get_height() * 0.42)
                if selected_piece == None:
                    drawHighlightPossiblePieces(screen, players[turn])
                else:
                    drawMovableSquares(screen, selected_piece[0])

        if selected_piece == None:
            drawSelector(screen, spaceship, x, y)
        
        drop_pos = drawDragPos(screen, board, selected_piece)    

        for event in pygame.event.get():
            if event.type == QUIT:              
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    escMenu(menu, names)

        pygame.display.update()
        mainClock.tick(60)
  

def winMenu(menu, name):
    mainClock.tick(60)
    menu.fill((0,0,0))
    drawstyle.drawBackground(menu, "menus/images/background.png")
    xRatio = 0.845
    yRatio = 0.125
    scale = 0.35
    logoEasterEgg = drawstyle.drawButton(menu, "menus/images/logo.png", xRatio, yRatio, scale)
    drawstyle.drawText("Spaceship      Chess", headerFont, textColor, menu, menu.get_width() * 0.1, menu.get_height() * 0.1)
    xRatio, yRatio = 0.225, 0.45
    drawstyle.drawText(name+" has won the game", subHeaderFont, textColor, menu, menu.get_width()*xRatio, menu.get_height()*yRatio)
    xRatio = 0.5
    yRatio = 0.9
    scale = 1
    returnButton = drawstyle.drawButton(menu, "menus/images/button_exit.png", xRatio, yRatio, scale)
    running = True
    while running:
        if returnButton.draw(menu):
            pygame.mixer.Sound.play(clickSound)
            pygame.quit()
            sys.quit()          
        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        mainClock.tick(60)  

mainMenu(screen)