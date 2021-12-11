import pygame
import copy
from random import choice, randint
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RIGHT, K_LEFT, K_DOWN, K_UP, K_z, K_s, K_q, K_d, MOUSEBUTTONDOWN


class Game:
    def __init__(self):
        self.width, self.height, self.multiplier, self.speed = 20, 20, 30, 2.5
        self.snake_pos = [[randint(0, self.width - 1), randint(0, self.height - 1)]]
        self.possible_pos = [[i, j] for i in range(self.width) for j in range(self.height)]
        self.running, self.eind, self.voeg_toe = False, False, False
        self.direction = ''
        self.fruit = [-1, -1]

    def longer(self):
        self.new_position()
        self.voeg_toe = True

    def new_position(self):
        possible = [i for i in self.possible_pos if i not in self.snake_pos]
        self.fruit = choice(possible)

    def end(self, screen):
        self.eind = True
        font, font2 = pygame.font.Font('font.ttf', 80), pygame.font.Font('font.ttf', 50)
        the_end_text, again_text = font.render('The end', True, (0, 0, 0)), font2.render('Go again', True, (0, 0, 0))
        the_end_text_rect, again_text_rect = the_end_text.get_rect(), again_text.get_rect()
        the_end_text_rect.center = ((self.width/2)*self.multiplier, (self.height/2)*self.multiplier)
        again_surface = pygame.surface.Surface((150, 60))
        again_surface.fill((255, 0, 0))
        pygame.draw.rect(again_surface, (0, 0, 0), again_surface.get_rect(), 1)
        again_text_rect.center = (again_surface.get_width()/2, again_surface.get_height()/2)
        pos_again = (((self.width/2)*self.multiplier - 75, (self.width/2)*self.multiplier + 75),
                     ((self.height/2)*self.multiplier + 35, 60 + (self.height/2)*self.multiplier + 35))
        screen.fill((255, 0, 0))
        screen.blit(the_end_text, the_end_text_rect)
        again_surface.blit(again_text, again_text_rect)
        screen.blit(again_surface, ((self.width / 2) * self.multiplier - 75, (self.height / 2) * self.multiplier + 35))
        pygame.display.flip()
        while self.eind:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.eind = False
                if (event.type == MOUSEBUTTONDOWN and pos_again[0][0] <= pygame.mouse.get_pos()[0] <= pos_again[0][1]
                        and pos_again[1][0] <= pygame.mouse.get_pos()[1] <= pos_again[1][1]):
                    self.__init__()
                    self.run()
                    return
        self.running = False

    def run(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        screen = pygame.display.set_mode((self.width * self.multiplier, self.height * self.multiplier))
        clock = pygame.time.Clock()
        self.running = True
        self.new_position()
        while self.running:
            self.speed += 0.01
            screen.fill((0, 0, 0))
            eerste = copy.copy(self.snake_pos[0])
            if self.voeg_toe:
                self.voeg_toe = False
            else:
                self.snake_pos.pop()
            if self.direction == 'R':
                eerste[0] += 1
                if eerste[0] >= self.width or eerste in self.snake_pos:
                    self.end(screen)
                    return
                if eerste == self.fruit:
                    self.longer()
            elif self.direction == 'U':
                eerste[1] -= 1
                if eerste == self.fruit:
                    self.longer()
                if eerste[1] < 0 or eerste in self.snake_pos:
                    self.end(screen)
                    return
            elif self.direction == 'L':
                eerste[0] -= 1
                if eerste == self.fruit:
                    self.longer()
                if eerste[0] < 0 or eerste in self.snake_pos:
                    self.end(screen)
                    return
            elif self.direction == 'D':
                eerste[1] += 1
                if eerste == self.fruit:
                    self.longer()
                if eerste[1] >= self.height or eerste in self.snake_pos:
                    self.end(screen)
                    return
            self.snake_pos.insert(0, eerste)
            pygame.draw.circle(screen, (0, 255, 0), (self.fruit[0] * self.multiplier + self.multiplier / 2,
                                                     self.fruit[1] * self.multiplier + self.multiplier / 2),
                               self.multiplier / 2)
            for i, e in enumerate(self.snake_pos):
                if i == 0:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (e[0] * self.multiplier, e[1] * self.multiplier, self.multiplier, self.multiplier),
                                     2)
                else:
                    pygame.draw.rect(screen, (0, 0, 255), (e[0] * self.multiplier, e[1] * self.multiplier,
                                                           self.multiplier, self.multiplier), 2)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_RIGHT or event.key == K_d:
                        if self.direction == 'L':
                            break
                        self.direction = 'R'
                    if event.key == K_LEFT or event.key == K_q:
                        if self.direction == 'R':
                            break
                        self.direction = 'L'
                    if event.key == K_UP or event.key == K_z:
                        if self.direction == 'D':
                            break
                        self.direction = 'U'
                    if event.key == K_DOWN or event.key == K_s:
                        if self.direction == 'U':
                            break
                        self.direction = 'D'
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


Game().run()
