import pygame


class Explosions:
    #handles the explosion animation of ships
    def __init__(self):
        self.explosion_list = []
        self.color_list = [(255, 215, 0), (182, 120, 35)]

    def spawn(self, co_list):
        for co in co_list:
            self.explosion_list.append([co[0], co[1], 0])

    def anim(self):
        for explosion in self.explosion_list:
            explosion[2] += 1
            if explosion[2] >= 25:
                self.explosion_list.remove(explosion)

    def draw(self, screen):
        for explosion in self.explosion_list:
            pygame.draw.circle(screen, self.color_list[explosion[2] % 2], (explosion[0], explosion[1]), 5 * explosion[2] // 2, 3)
