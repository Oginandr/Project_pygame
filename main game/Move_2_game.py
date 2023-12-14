import numpy as np
import math
import random
import pygame
import pygame.gfxdraw

FPS = 60

BLACK = (0, 0, 0)
RED = 0xFF0000
WHITE = 0xFFFFFF
GREEN = 0X32CD32

""" Размеры экрана """
WIDTH = 1200
HEIGHT = 700

class Ball:
    """ Класс главного управляемого шара """
    
    def __init__(self, screen):
        """ Определение начальных параметров шара:
            x, y - координаты
            r - радиус
            vx, vy - проекции скорости на координатные оси
            V - фиксированный модуль скорости при движении """
        
        self.screen = screen
        self.x = random.randint(50, 150)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.V = 8
        
    def move(self):
        """ Функция задающая движение шара в направлении положения курсора """
        
        pos_mouse = pygame.mouse.get_pos()
        if ((pos_mouse[0] - self.x) ** 2 + (pos_mouse[1] - self.y) ** 2) > self.r ** 2:
            self.vx = self.V * (pos_mouse[0] - self.x) / ((pos_mouse[0] - self.x) ** 2 + (pos_mouse[1] - self.y) ** 2) ** 0.5
            self.vy = self.V * (pos_mouse[1] - self.y) / ((pos_mouse[0] - self.x) ** 2 + (pos_mouse[1] - self.y) ** 2) ** 0.5
            self.x += self.vx
            self.y += self.vy
            
    def hit(self, enemy):
        """ Функция, проверяющая, столкнулся ли шар с каким-либо из врагов """
        
        if ((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2) ** 0.5 <= enemy.r + self.r:
            return True
        else:
            return False
        
    def draw(self):
        """ Функция отображающая шар на экране в соответствующем его координатам месте
            Используется градиернтная раскраска шара """

        for r in np.linspace(0, self.r, 100):
            alpha = int(135 * (1 - r / self.r))
            color = (0, 0, 255 - alpha)
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.r - r), color)

        

class Rocket:
    """ Класс самонаводящихся врагов, условно ракета """
    
    def __init__(self, screen):
        """ Определение начальных параметров ракеты:
            x, y - координаты
            r - радиус
            vx, vy - проекции скорости на координатные оси
            V - фиксированный модуль скорости при движении """
        
        self.screen = screen
        self.x = random.randint(400, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = random.randint(10, 20)
        self.vx = 0
        self.vy = 0
        self.V = 4
        
    def move(self, ball):
        """ Функция движения рокеты в направлении цели (главного шара) """
        
        self.vx = self.V * (ball.x - self.x) / ((ball.x - self.x) ** 2 + (ball.y - self.y) ** 2) ** 0.5
        self.vy = self.V * (ball.y - self.y) / ((ball.x - self.x) ** 2 + (ball.y - self.y) ** 2) ** 0.5
        self.x += self.vx
        self.y += self.vy

    def hit(self, obj):
        """ Функция, проверяющая, столкнулась ли ракета с другим объектом obj """
        
        if ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5 <= obj.r + self.r:
            return True
        else:
            return False
        
    def draw(self):
        """ Функция отображающая ракету (шар) на экране в соответствующем ее координатам месте
            Используется градиернтная раскраска шара """
        
        for r in np.linspace(0, self.r, 100):
            alpha = int(135 * (1 - r / self.r))
            color = (255 - alpha, 0, 0)
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.r - r), color)
    
        
class Meteor:
    """ Класс примитивных врагов, условно метеоры """
    
    def __init__(self, screen):
        """ Определение начальных параметров метеора:
            x, y - координаты
            r - радиус
            vx, vy - проекции скорости на координатные оси """
        
        self.screen = screen
        self.x = random.randint(400, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = random.randint(10, 20)
        self.vx = random.randint(- 5, 5)
        self.vy = random.randint(- 5, 5)

    def move(self):
        """ Функция движения метеора равномерно прямолинейно с учетом отскакивания от стен """
        
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
        """ Функция, проверяющая, столкнулся ли метеор с другим объектом obj """
        
        if ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5 <= obj.r + self.r:
            return True
        else:
            return False
            
    def draw(self):
        """ Функция отображающая метеор (шар) на экране в соответствующем ее координатам месте
            Используется градиернтная раскраска шара """

        for r in np.linspace(0, self.r, 100):
            alpha = int(135 * (1 - r / self.r))
            color = (0, 255-alpha, 0)
            pygame.gfxdraw.filled_circle(screen, self.x, self.y, int(self.r - r), color)


class Bonus(Meteor):
    """ Класс бонусов, наследующий класс Meteor"""
    
    def __init__(self, screen):
        """ Определение начальных параметров бонуса:
            x, y - координаты
            r - радиус
            """
        Meteor.__init__(self, screen)
        self.screen = screen
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.r = 10
    
    def hit(self, obj):
        """ Функция, проверяющая, столкнулся ли бонус с другим объектом obj """
        """
        if ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5 <= obj.r + self.r:
            return True
        else:
            return False
        """
        return super().hit(obj)
            
    def draw(self):
        """ Функция отображающая бонус (шар) на экране в соответствующем ее координатам месте
            Используется градиернтная раскраска шара """
        
        for r in np.linspace(0, self.r, 100):
            alpha = int(135 * (1 - r / self.r))
            color = (255-alpha, 255-alpha/4, 0)
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.r - r), color)
        pygame.draw.line(screen, RED, [self.x - self.r, self.y], [self.x + self.r, self.y], 1)
        pygame.draw.line(screen, RED, [self.x, self.y - self.r], [self.x, self.y + self.r], 1)
        pygame.draw.circle(
            self.screen,
            0xFF03B8,
            (self.x, self.y),
            self.r, 1
        )


""" Инициализация игрового пространства """
       
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

finished = False

""" Создание игровых объектов как элементов соответствующих классов """

ball = Ball(screen)

bonuses = []

N_meteors = 4
meteors = set()
for i in range(N_meteors):
    meteors.add(Meteor(screen))

N_rockets = 4
rockets = set()
for j in range(N_rockets):
    rockets.add(Rocket(screen))

""" Определение массива движения шара, множеств уничтоженных врагов и собранных бонусов (обновляемого),
    таймера добавления врагов, добавления и удаления бонусов, счётчика очков """

dead_meteors = set()
dead_rockets = set()
dead_bonuses = set()

enemy_time = 0

bonus_time = 0
bonus_time_life = 0

score = 0

""" Главный цикл 2 режима игры """

while not finished:
    screen.fill(WHITE)

    """ Отрисовка объектов """

    screen.blit(pygame.font.SysFont('Verdana', 30).render(str(score), False, (0, 0, 0)), (30, 20))

    ball.draw()
    for meteor in meteors:
        meteor.draw()
    for rocket in rockets:
        rocket.draw()
    for bonus in bonuses:
        bonus.draw()

    """ Закрытие игры при нажатии на "крестик" """
    pygame.key.set_repeat(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True        

    """ Проверка объектов на столкновения """
    
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

    for bonus in set(bonuses):
        if bonus.hit(ball):
            dead_bonuses.add(bonus)
            score += int(1 * (8 - bonus_time_life / FPS))
            if meteors != set():
                meteors.pop()
            if rockets != set():
                rockets.pop()
                
    """
    for rocket_1 in rockets:
        for rocket_2 in rockets:
            if (rocket_1 != rocket_2) and (rocket_1.hit(rocket_2)):
                dead_rockets.add(rocket_1)
                dead_rockets.add(rocket_2)
    """

    """ Удаление уничтоженных врагов """
    
    meteors -= dead_meteors
    rockets -= dead_rockets
    bonuses = list(set(bonuses) - dead_bonuses)

    """ Движение объектов """
    
    for meteor in meteors:
        meteor.move()
    for rocket in rockets:
        rocket.move(ball)

    ball.move()

    """ Периодическое добавление врагов, добавление и удаление бонусов """

    if enemy_time < 300:
        enemy_time += 1
    elif enemy_time == 300:
        enemy_time = 0
        rockets.add(Rocket(screen))
        meteors.add(Meteor(screen))

    if bonus_time < FPS * 4:
        bonus_time += 1
    elif bonus_time == FPS * 4:
        bonus_time = 0
        bonuses.append(Bonus(screen))
        
    if bonus_time_life < FPS * 8:
        bonus_time_life += 1
    elif bonus_time_life == FPS * 8:
        bonus_time_life = 0
        if bonuses != []:
            bonuses.pop(0)
        

    pygame.display.update()
    clock.tick(FPS)
                
pygame.quit()
