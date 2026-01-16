import pygame


class Ship:
    #the class of the player
    def __init__(self, x, y):
        self.velocity = [0, 0]
        self.speed = 7
        self.list_images = [pygame.transform.scale(pygame.image.load("assets/textures/ship/ship" + str(i) + ".png"), (42, 42)) for i in range(4)]
        self.image = self.list_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.health = 5
        self.heart = pygame.transform.scale(pygame.image.load("assets/textures/gui/heart.png"), (32, 32))
        self.heart_rect = self.heart.get_rect()

        self.points = 0

        self.shout_list = []
        self.bullets = 20
        self.charging = 0
        self.press0 = False

    def get_joystick(self, event, sound):
        #handles joystick inputs
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0 or event.axis == 1:
                self.velocity[event.axis] = round(event.value, 0)
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1 and self.bullets > 0 and self.charging == 0:
                self.shout_list.append(pygame.Rect(self.rect.centerx + 3, self.rect.centery - 7, 2, 20))
                self.shout_list.append(pygame.Rect(self.rect.centerx - 5, self.rect.centery - 7, 2, 20))
                self.bullets -= 1
                sound.play("ship_laser_blast", 1)
            if event.button == 0:
                self.press0 = True
                sound.play("recharging", 1)
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0: #you have to stay pressin 'O' to charge
                self.press0 = False
                self.charging = 0
                sound.stop(1)

    def move(self):
        c = self.rect.center
        if (c[0] >= 21) and (c[0] <= 579):
            self.rect.move_ip(self.speed * self.velocity[0], 0)
        elif c[0] < 21:
            self.rect.move_ip(1, 0)
        elif c[0] > 579:
            self.rect.move_ip(-1, 0)
        if (c[1] >= 21) and (c[1] <= 779):
            self.rect.move_ip(0, self.speed * self.velocity[1])
        elif c[1] < 21:
            self.rect.move_ip(0, 1)
        elif c[1] > 779:
            self.rect.move_ip(0, -1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.charging > 0:
            pygame.draw.rect(screen, (58, 242, 75), pygame.Rect(self.rect.centerx - 21, self.rect.centery + 30, 42 * self.charging/100, 10))

    def tp(self, x, y):
        #put the player at the coords (x, y)
        c = self.rect.center
        self.rect.move_ip(-c[0], -c[1])
        self.rect.move_ip(x, y)

    def move_shout(self):
        for shout in self.shout_list:
            shout.move_ip(0, -6)
            if shout.centery + 15 <= 0:
                self.shout_list.remove(shout)
        if self.press0:
            self.charging += 1
            if self.charging >= 100:
                self.bullets = 20
                self.charging = 0
                self.press0 = False

    def draw_shouts(self, screen):
        for shout in self.shout_list:
            pygame.draw.rect(screen, (240, 195, 0), shout)

    def del_list_shout(self, list_s):
        #delete the shouts of the player that are off screen
        for s in list_s:
            if s in self.shout_list:
                self.shout_list.remove(s)

    def collisions(self, shout_list, sound):
        del_shout = []
        explosions_co = []
        for shout in shout_list:
            if shout.colliderect(self.rect):
                self.health -= 1
                self.points -= 500
                sound.play("explosion", 2)
                del_shout.append(shout)
                explosions_co.append(self.rect.center)

        return del_shout, explosions_co

    def draw_life(self, screen):
        #displays the health of the player
        self.heart_rect.move_ip(-self.heart_rect.centerx + 20, -self.heart_rect.centery + 20)
        for i in range(self.health):
            screen.blit(self.heart, self.heart_rect)
            self.heart_rect.move_ip(0, 40)
