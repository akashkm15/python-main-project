import pygame
import random  # for generating random numbers
import sys  # for exiting the program
from pygame.locals import *  # basic pygame imports

# global variables for the game

FPS = 32
SCREENWIDTH = 1000
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = "E://python//projects//project-2//sprites//bird.png"
BACKGROUND = "E://python//projects//project-2//sprites//background.png"
PIPE = "E://python//projects//project-2//sprites//pipe.png"


def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    # create 2 pipes  for  blitting on the  screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list for upper pipe
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # lists for lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flaping
    playerFlapped = False  # it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

        # score check
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVely < playerMaxVelY and not playerFlapped:
            playerVely += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        # moving pipes to the left
        for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
            upperPipes['x'] += pipeVelx
            lowerPipes['x'] += pipeVelx

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipes['x'], upperPipes['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipes['x'], lowerPipes['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
       Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
       """

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENWIDTH - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipe
        {'x': pipeX, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == "__main__":  # main function
    pygame.init()  # initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Akash')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('E://python//projects//project-2//sprites//0.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//1.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//2.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//3.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//4.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//5.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//6.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//7.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//8.png').convert_alpha(),
        pygame.image.load('E://python//projects//project-2//sprites//9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('E://imgs//WallpaperDog-20487414.jpg').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('E://python//projects//project-2//sprites//base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha())

    # game sounds

    GAME_SOUNDS['die'] = pygame.mixer.Sound('E://python//projects//project-2//audio//die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('E://python//projects//project-2//audio//hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('E://python//projects//project-2//audio//point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('E://python//projects//project-2//audio//swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('E://python//projects//project-2//audio//wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  # show welcome screen to the user
        mainGame()  # this is main game function
