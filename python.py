import random
import pygame
import sys
from pygame.locals import *

screen_X = 640
screen_Y = 480

#Define snake parameters
class Snake(object):
    def __init__(self):
        self.direction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.snakePosition()   #The initial length is five

    def snakePosition(self):
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        position = pygame.Rect(left, top, 20, 20)   #The initial position
        if self.direction == pygame.K_RIGHT:
            position.left += 20
        elif self.direction == pygame.K_LEFT:
            position.left -= 20
        elif self.direction == pygame.K_UP:
            position.top -= 20
        elif self.direction == pygame.K_DOWN:
            position.top += 20
        self.body.insert(0, position)
    #The end node is removed when the snake moves
    def delNode(self):
        self.body.pop()
    #detect if snake dead
    def isDead(self):
        if self.body[0].x not in range(screen_X):
            return True
        if self.body[0].y not in range(screen_Y):
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False

    def move(self):
        self.snakePosition()
        self.delNode()

    def changeDirection(self, curKey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curKey in LR + UD:   #can't just go in the opposite direction
            if (curKey in LR) and (self.direction in LR):
                return
            if (curKey in UD) and (self.direction in UD):
                return
            self.direction = curKey

#Define target parameters
class Target(object):
    def __init__(self):
        self.rect = pygame.Rect(-20, 0, 20, 20)     #Initial value

    def remove(self):
        self.rect.x = -20

    def set(self):
        if self.rect.x == -20:
            xPos = []
            yPos = []
            for pos in range(20, screen_X - 20, 20):    #Randomly generated
                xPos.append(pos)
            for pos in range(20, screen_Y - 20, 20):
                yPos.append(pos)
            self.rect.left = random.choice(xPos)
            self.rect.top = random.choice(yPos)

#Define font text
def show_text(screen, pos, text, color, font_bold=False, font_size=20, font_italic=False):
    cur_font = pygame.font.SysFont('arial', font_size)  #Font and size
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)

def draw_Grid():
	for x in range(0, 640, 20):
		pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 480))
	for y in range(0, 480, 20):
		pygame.draw.line(screen, (40, 40, 40), (0, y), (640, y))

#end function
def gameOver():
    pygame.quit()
    sys.exit()

#entry function
def main():
    global screen
    #initialize pygame
    pygame.init()
    #define speed
    fpsClock = pygame.time.Clock()
    #create interface
    screenSize = (screen_X, screen_Y)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Snake Game')
    #initialize variates
    scores = 0
    isdead = False
    snake = Snake()
    target = Target()
    #define events
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameOver()
            if event.type == pygame.KEYDOWN:
                snake.changeDirection(event.key)
                if event.key == pygame.K_SPACE and isdead:
                    return main()

        screen.fill((0, 0, 0))  #screen color
        draw_Grid()
        #detect if snake dead
        if not isdead:
            snake.move()
        for rect in snake.body: #draw snakebody
            pygame.draw.rect(screen, (0, 255, 0), rect, 0)

        isdead = snake.isDead()

        if isdead:
            show_text(screen, (150, 180), 'YOU DEAD!', (255, 0, 0), False, 70)
            show_text(screen, (175, 240), 'press space to try again', (255, 255, 255), False, 30)

        #detect eating target
        if target.rect == snake.body[0]:
            scores += 1
            target.remove()
            snake.snakePosition()
        target.set()
        while target.rect in snake.body:    #Avoid target refresh in snake body
            target.remove()
            target.set()
        pygame.draw.rect(screen, (255, 0, 0), target.rect, 0)

        show_text(screen, (550, 50), 'Scores: ' + str(scores), (255, 255, 255))
        pygame.display.update()
        fpsClock.tick(10)

main()