import pygame
from random import randint


class Stars:
    def __init__(self):
        self.color_list = [(255, 255, 255), (200, 200, 200)]
        self.star_list = [[pygame.Rect(randint(0, 600), 6 * i, 1, 1), self.color_list[randint(0, 1)]] for i in range(150)]

    def spawn(self):
        #spawns the stars randomly on the background
        if pygame.time.get_ticks() % 6 == 0:
            self.star_list.append([pygame.Rect(randint(0, 600), 0, 1, 1), self.color_list[randint(0, 1)]])

    def move(self):
        #moves the stars
        for star in self.star_list:
            star[0].move_ip(0, 1)
            if star[0].centery >= 801:
                self.star_list.remove(star)

    def draw(self, screen):
        for star in self.star_list:
            pygame.draw.rect(screen, star[1], star[0])
