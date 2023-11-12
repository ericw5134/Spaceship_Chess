import pygame

def drawEscMenu(menu):
    running = True

    while running:
        menu.fill((52, 78, 91))
        '''
        resumeImg = pygame.image.load("images/button_back.png").convert_alpha()
        resumeDim = resumeImg.get_rect()    # Get the dimensions of the img
        resumeX = (menu.get_width() - resumeDim.width) // 2   # Calculate the position to center the image
        resumeY = (menu.get_height() - resumeDim.height) * 0.30
        resumeButton = button.Button(resumeX, resumeY, resumeImg, 1)

        quitImg = pygame.image.load("images/button_quit.png").convert_alpha()
        quitDim = quitImg.get_rect()
        quitX = (menu.get_width() - quitDim.width) // 2
        quitY = (menu.get_height() - quitDim.height) * 0.70
        quitButton = button.Button(quitX, quitY, quitImg, 1)

        optionsImg = pygame.image.load("images/button_options.png").convert_alpha()
        optionsDim = optionsImg.get_rect()
        optionsX = (menu.get_width() - optionsDim.width) // 2
        optionsY = (menu.get_height() - optionsDim.height) * 0.50
        optionsButton = button.Button(optionsX, optionsY, optionsImg, 1)

        resumeButton.draw(menu)
        optionsButton.draw(menu)
        quitButton.draw(menu) 
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


