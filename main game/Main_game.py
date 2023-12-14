
from importlib import reload

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

""" Загрузка изображений """

pic_arrows = pygame.transform.scale(pygame.image.load('arrows.png'), (200 * 0.8,  116 * 0.8))
pic_cursor = pygame.transform.scale(pygame.image.load('cursor.png'), (120 * 0.8,  120 * 0.8))
pic_space = pygame.transform.scale(pygame.image.load('space.png'), (150 * 0.8,  68 * 0.8))

class Buttons:
    """ Класс кнопок выбора режима игры """
    
    def __init__(self, screen):
        """ Определение параметров первой (левой) кнопки:
            x, y - координаты левого верхнего края
            h, l - выстоа и ширина"""
        
        self.screen = screen
        self.x = 200
        self.y = 280
        self.h = 100
        self.l = 200
        
    def draw(self):
        """ Функция отрисовки 3 кнопок с помещением в них текста с номером режима """
        
        for i in range(3):
            pygame.draw.rect(self.screen, BLACK, 
                     (self.x + i * 300, self.y, self.l, self.h), 2)
            screen.blit(pygame.font.SysFont('Verdana', 20).render(str(i + 1) + ' режим игры', False, (0, 0, 0)), (self.x + 28 + i * 300, self.y + 38))
            screen.blit(pic_arrows, (self.x + 20, self.y + self.h + 30))
            screen.blit(pic_cursor, (self.x + 355, self.y + self.h + 30))
            screen.blit(pic_arrows, (self.x + 620, self.y + self.h + 20))
            screen.blit(pic_space, (self.x + 640, self.y + self.h + 130))
            
    def mouse_to_button(self):
        """ Функция проверки попадания курсором на одну из 3-х кнопок """
        
        pos_mouse = pygame.mouse.get_pos()
        if  (self.x < pos_mouse[0] < self.x + self.l) and (self.y < pos_mouse[1] < self.y + self.h):
            return(1)
        elif (self.x + 300 < pos_mouse[0] < self.x + self.l + 300) and (self.y < pos_mouse[1] < self.y + self.h):
            return(2)
        elif (self.x + 600 < pos_mouse[0] < self.x + self.l + 600) and (self.y < pos_mouse[1] < self.y + self.h):
            return(3)
        else:
            return(0)


""" Главный цикл """

game_finished = False

first_start = [0, 0, 0]

while not game_finished:

    """ Инициализация игрового пространства """
    
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    """ Создание кнопок как объектов игрового пространства """

    buttons = Buttons(screen)

    game_mode = 0

    all_finished = False

    """ Цикл отрисовки экрана выбора режима """
    
    while not all_finished:
        screen.fill(WHITE)

        """ Отрисовка кнопок """
    
        buttons.draw()

        """ Приверка нажатия на кнопку выбора одного из режимов """
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                all_finished = True
                game_finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.mouse_to_button() > 0:
                    all_finished = True
                    game_mode = buttons.mouse_to_button()
        
        pygame.display.update()
        clock.tick(FPS)

    """ Запускается выбранный пользователем режим """
    
    if game_mode == 1:
        if first_start[0] == 0:
            import Move_1_game
            first_start[0] = 1
        else:
            import Move_1_game
            Move_1_game = reload(Move_1_game)
    elif game_mode == 2:
        if first_start[1] == 0:
            import Move_2_game
            first_start[1] = 1
        else:
            import Move_2_game
            Move_2_game = reload(Move_2_game)
    elif game_mode == 3:
        if first_start[2] == 0:
            import Move_3_game
            first_start[2] = 1
        else:
            import Move_3_game
            Move_3_game = reload(Move_3_game)
            
"""
    Move_1_game = reload(Move_1_game)
    Move_2_game = reload(Move_2_game)
    Move_3_game = reload(Move_3_game)
"""
pygame.quit()


    
    


