import numpy as np
import math
import random
import pygame

FPS = 60

BLACK = (0, 0, 0)
RED = 0xFF0000
WHITE = 0xFFFFFF
GREEN = 0X32CD32

WIDTH = 1200
HEIGHT = 700

class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(50, 150)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.V = 8
        
    def move(self):
        """
        if (0 + self.r < self.x + motion[0] < WIDTH - self.r) and (0 + self.r < self.y + motion[1] < HEIGHT - self.r):
            self.x += motion[0]
            self.y += motion[1]
        """
        #if event:
        pos_mouse = pygame.mouse.get_pos()
        if ((pos_mouse[0] - self.x) ** 2 + (pos_mouse[1] - self.y) ** 2) > self.r ** 2:
            self.vx = self.V * (pos_mouse[0] - self.x) / ((pos_mouse[0] - self.x) ** 2 + (pos_mouse[1] - self.y) ** 2) ** 0.5
            self.vy = self.V * (pos_mouse[1] - self.y) / ((pos_mouse[0] - self.x) ** 2 + (pos_mouse[1] - self.y) ** 2) ** 0.5
            self.x += self.vx
            self.y += self.vy
            
    def hit(self, enemy):
            if ((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2) ** 0.5 <= enemy.r + self.r:
                return True
            else:
                return False
        
    def draw(self):
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r
        )

class Rocket:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(400, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = random.randint(10, 20)
        self.vx = 0
        self.vy = 0
        self.V = 4
        
    def move(self, ball):
        
        self.vx = self.V * (ball.x - self.x) / ((ball.x - self.x) ** 2 + (ball.y - self.y) ** 2) ** 0.5
        self.vy = self.V * (ball.y - self.y) / ((ball.x - self.x) ** 2 + (ball.y - self.y) ** 2) ** 0.5
        self.x += self.vx
        self.y += self.vy

    def hit(self, obj):
        if ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5 <= obj.r + self.r:
            return True
        else:
            return False
        
    def draw(self):
        pygame.draw.circle(
            self.screen,
            RED,
            (self.x, self.y),
            self.r
        )
    
        
class Meteor:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(400, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = random.randint(10, 20)
        self.vx = random.randint(- 5, 5)
        self.vy = random.randint(- 5, 5)

    def move(self):
        
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        if self.r < new_x < WIDTH - self.r:
            self.x = new_x
        else:
            self.vx = - self.vx
        self.x += self.vx
        if self.r < new_y < HEIGHT - self.r:
            self.y = new_y
        else:
            self.vy = - self.vy

    def hit(self, obj):
        if ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5 <= obj.r + self.r:
            return True
        else:
            return False
            
    def draw(self):
        pygame.draw.circle(
            self.screen,
            GREEN,
            (self.x, self.y),
            self.r
        )
        
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

finished = False

ball = Ball(screen)

N_meteors = 6
meteors = set()
for i in range(N_meteors):
    meteors.add(Meteor(screen))

N_rockets = 6
rockets = set()
for j in range(N_rockets):
    rockets.add(Rocket(screen))

motion = [0, 0]

dead_meteors = set()
dead_rockets = set()

while not finished:
    screen.fill(WHITE)
    ball.draw()
    for meteor in meteors:
        meteor.draw()
    for rocket in rockets:
        rocket.draw()
        
    pygame.key.set_repeat(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion[0] = - 8
            elif event.key == pygame.K_RIGHT:
                motion[0] = + 8
            elif event.key == pygame.K_UP:
                motion[1] = - 8
            elif event.key == pygame.K_DOWN:
                motion[1] = + 8
        """
            
        #if event.type == pygame.MOUSEMOTION:
        
    
    for meteor in meteors:
        if ball.hit(meteor):
            finished = True
    for rocket in rockets:
        if ball.hit(rocket):
            finished = True
    
    for meteor in meteors:
        for rocket in rockets:
            if meteor.hit(rocket):
                dead_meteors.add(meteor)
                dead_rockets.add(rocket)
               
    for meteor_1 in meteors:
        for meteor_2 in meteors:
            if (meteor_1 != meteor_2) and (meteor_1.hit(meteor_2)):
                dead_meteors.add(meteor_1)
                dead_meteors.add(meteor_2)
                
    """
    for rocket_1 in rockets:
        for rocket_2 in rockets:
            if (rocket_1 != rocket_2) and (rocket_1.hit(rocket_2)):
                dead_rockets.add(rocket_1)
                dead_rockets.add(rocket_2)
    """
    
    meteors -= dead_meteors
    rockets -= dead_rockets
    
    for meteor in meteors:
        meteor.move()
    for rocket in rockets:
        rocket.move(ball)

    ball.move()
    #ball.move(motion)
    #motion = [0, 0]

    pygame.display.update()
    clock.tick(FPS)
                
pygame.quit()
