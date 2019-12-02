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
