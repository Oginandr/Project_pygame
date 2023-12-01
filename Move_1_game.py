import numpy as np
import math
import random
import pygame

FPS = 60

BLACK = (0, 0, 0)
RED = 0xFF0000
WHITE = 0xFFFFFF

WIDTH = 1200
HEIGHT = 700

class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(50, 150)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = 10
        
    def move(self, motion):
        
        self.x += motion[0]
        self.y += motion[1]
        
    def hit(self, meteor):
            if ((meteor.x - self.x) ** 2 + (meteor.y - self.y) ** 2) ** 0.5 <= meteor.r + self.r:
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
class Meteors:
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
    def draw(self):
        pygame.draw.circle(
            self.screen,
            RED,
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
meteors = []
for i in range(N_meteors):
    meteors.append(Meteors(screen))

motion = [0, 0]

while not finished:
    screen.fill(WHITE)
    ball.draw()
    for i in range(N_meteors):
        meteors[i].draw()

    pygame.key.set_repeat(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion[0] = - 8
            elif event.key == pygame.K_RIGHT:
                motion[0] = + 8
            elif event.key == pygame.K_UP:
                motion[1] = - 8
            elif event.key == pygame.K_DOWN:
                motion[1] = + 8
    
    for i in range(N_meteors):
        if ball.hit(meteors[i]):
            finished = True
    
    for i in range(N_meteors):
        meteors[i].move()
    ball.move(motion)
    motion = [0, 0]

    pygame.display.update()
    clock.tick(FPS)
                
pygame.quit()
