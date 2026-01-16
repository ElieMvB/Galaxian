import pygame
from random import randint


class Enemy:
    def __init__(self):
        self.enemy_list = []
        self.shout_list = []
        self.spawn_prob = 60
        self.death = 0
        self.images = [pygame.transform.scale(pygame.image.load("assets/textures/enemy/enemy" + str(i) + ".png"), (42, 42)) for i in range(2)]

    def spawn(self, sound):
        #spawns the new ships against the player
        if self.death >= 50:
            self.death = 0
            if self.spawn_prob > 2:
                self.spawn_prob -= 2
            sound.play("dong", 6)
        if randint(0, self.spawn_prob) == 0:
            i = randint(0, 1)
            r = self.images[i].get_rect(x = randint(0, 558), y = -42)
            self.enemy_list.append([self.images[i], r, 3 + 1 * i, 0])
            #an ennemy is defined with the following list : [image, rect, speed, velocity]

    def draw(self, screen):
        #displays the differents enemies on the screen
        for shout in self.shout_list:
            pygame.draw.rect(screen, (255, 0, 0), shout)
        for enemy in self.enemy_list:
            screen.blit(enemy[0], enemy[1])

    def move(self, sound):
        points = 0
        for enemy in self.enemy_list:
            enemy[1].move_ip(0, enemy[2]) #moves to the bottom the ennemy ship
            if enemy[2] == 4: #what means this enemy is a ship that also can move horizontaly
                if enemy[1].centerx <= 7:
                    enemy[3] = 1
                elif enemy[1].centerx >= 593:
                    enemy[3] = -1
                elif randint(0, 30) == 0:
                    enemy[3] = randint(-1, 1)
                enemy[1].move_ip(3 * enemy[3], 0)
                if randint(0, 30) == 0:
                    self.shout_list.append(pygame.Rect(enemy[1].centerx + 20, enemy[1].centery, 2, 15))
                    self.shout_list.append(pygame.Rect(enemy[1].centerx - 21, enemy[1].centery, 2, 15))
                    sound.play("enemy_laser_blast" + str(randint(0, 2)), 3)
            if enemy[1].centery >= 842:
                self.enemy_list.remove(enemy)
                points -= 250 #the player loses points when a ship cross the screen
        for shout in self.shout_list:
            shout.move_ip(0, 6)
        return points

    def collisions(self, ship_rect, shout_list, sound):
        sub_life = 0
        sub_shout = []
        explosion_co = []
        points = 0
        for enemy in self.enemy_list:
            if enemy[1].colliderect(ship_rect):
                sub_life += 1 #the health the player will lose
                points -= 500
                self.enemy_list.remove(enemy)
                explosion_co.append(ship_rect.center)
            for shout in shout_list:
                if enemy[1].colliderect(shout):
                    if enemy in self.enemy_list:
                        self.enemy_list.remove(enemy)
                        sound.play("enemy_explosion", 5)
                    sub_shout.append(shout)
                    explosion_co.append(enemy[1].center)
                    points += 1000 + 500 * (enemy[2] - 4) #the player wins mor points depending on what type is the ship
                    self.death += 1

        return sub_life, sub_shout, explosion_co, points

    def del_list_shout(self, list_s):
        for s in list_s:
            self.shout_list.remove(s)