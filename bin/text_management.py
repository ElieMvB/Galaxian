import pygame


class TextManagement:
    def __init__(self):
        self.size = 20
        self.font = pygame.font.Font('freesansbold.ttf', self.size)

    def print_text(self, screen, xy, t, colors, size = 20):
        #t = the text
        #prints the text on the screen using a pygame class
        if size != 20:
            self.font = pygame.font.Font('freesansbold.ttf', size)
        for i in range(len(t)):
            text = self.font.render(t[i], True, colors[0], colors[1])
            rect = text.get_rect()
            rect.center = (xy[0], xy[1] + (size + 7) * i)
            screen.blit(text, rect)
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
