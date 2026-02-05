import pygame
from time import time
from bin.class_ship import*
from bin.text_management import*
from bin.class_enemy import*
from bin.class_explosion import*
from bin.class_stars import*
from bin.sound_management import*


class Game:
    def __init__(self):
        #initialiation of the variables
        self.running = True
        self.screen = pygame.display.set_mode((600, 800))
        pygame.display.set_caption('Galaxian')
        pygame.display.set_icon(pygame.image.load('./assets/textures/ship/ship0.png'))
        self.clock = pygame.time.Clock()
        self.state = "Menu"
        self.time = time()
        #initialise the game controlers connected to the computer
        self.joy = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        #initialisation of the differents objects
        self.ship = Ship(300, 400)
        self.enemy = Enemy()
        self.explosions = Explosions()
        self.stars = Stars()

        self.text = TextManagement()
        self.sound = SoundManagement()

    def handling_events(self):
        #handles the inputs of the controler
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == "Menu":
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 2:
                        self.state = "Game"
                        self.sound.channels[7].set_volume(0.65)
                        self.ship.bullets = 20
                    if event.button == 4:
                        self.ship.image = self.ship.list_images[self.ship.list_images.index(self.ship.image) - 1]
                    elif event.button == 5:
                        i = self.ship.list_images.index(self.ship.image)
                        if i == len(self.ship.list_images) - 1:
                            self.ship.image = self.ship.list_images[0]
                        else:
                            self.ship.image = self.ship.list_images[i + 1]
                    self.ship.get_joystick(event, self.sound)
            elif self.state == "Game":
                self.ship.get_joystick(event, self.sound)
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        self.state = "Pause"
                        self.sound.channels[7].set_volume(0.8)
            elif self.state == "Game Over":
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 2:
                        self.state = "Menu"
                        self.ship = Ship(300, 400)
                        self.enemy = Enemy()
                        self.sound.channels[7].set_volume(0.8)
            elif self.state == "Pause":
                if event.type == pygame.JOYBUTTONDOWN:
                    self.state = "Game"
                    self.sound.channels[7].set_volume(0.65)

    def update(self):
        #background
        self.stars.spawn()
        self.stars.move()
        #plays music
        if not(self.sound.channels[7].get_busy()) and self.state != "Game Over":
            self.sound.channels[7].play(self.sound.sounds["Musics"][randint(0, len(self.sound.sounds["Musics"]) - 1)])
        #updates depending of the state of the game
        if self.state == "Menu":
            self.ship.move_shout()
        elif self.state == "Game":
            self.ship.move()
            self.ship.move_shout()
            self.enemy.spawn(self.sound)
            self.ship.points += self.enemy.move(self.sound) #the player loses points if an ennemy cross the screen
            #handles collisions with the other ships and the player
            colE = self.enemy.collisions(self.ship.rect, self.ship.shout_list, self.sound)
            colS = self.ship.collisions(self.enemy.shout_list, self.sound)
            self.ship.health -= colE[0]
            self.ship.points += colE[3]
            if self.ship.points < 0:
                self.ship.points = 0
            if colE[0] > 0:
                self.sound.play("explosion", 2)
            self.ship.del_list_shout(colE[1])
            self.enemy.del_list_shout(colS[0])
            self.explosions.spawn(colE[2] + colS[1])
            self.explosions.anim()
            if self.ship.health <= 0:
                self.state = "Death Anim"
                self.sound.channels[7].fadeout(1500)
                self.time = time()
        elif self.state == "Death Anim":
            self.explosions.anim()
            if time() - self.time > 0.5:
                self.state = "Game Over"

    def display(self):
        self.screen.fill((0, 0, 0))
        self.stars.draw(self.screen)
        if self.state == "Menu":
            self.text.print_text(self.screen, (550, 775), [str(self.ship.bullets)], ((255, 255, 255), (0, 0, 0)))
            self.text.print_text(self.screen, (300, 125), ["Appuyez sur 'X' pour commencer"], ((240, 195, 0), (0, 0, 0)), 35)
            self.ship.draw_shouts(self.screen)
            self.ship.draw(self.screen)
        elif self.state == "Game":
            self.text.print_text(self.screen, (550, 775), [str(self.ship.bullets)], ((255, 255, 255), (0, 0, 0)))
            self.text.print_text(self.screen, (50, 775), [str(self.ship.points)], ((255, 255, 255), (0, 0, 0)))
            self.enemy.draw(self.screen)
            self.ship.draw_shouts(self.screen)
            self.ship.draw(self.screen)
            self.ship.draw_life(self.screen)
            self.explosions.draw(self.screen)
        elif self.state == "Death Anim":
            self.text.print_text(self.screen, (50, 775), [str(self.ship.points)], ((255, 255, 255), (0, 0, 0)))
            self.enemy.draw(self.screen)
            self.ship.draw_shouts(self.screen)
            self.ship.draw(self.screen)
            self.explosions.draw(self.screen)
        elif self.state == "Game Over":
            self.text.print_text(self.screen, (50, 775), [str(self.ship.points)], ((255, 255, 255), (0, 0, 0)))
            self.text.print_text(self.screen, (300, 100), ["Game Over", "", "Appuyez sur 'X' pour revenir au menu"], ((255, 255, 255), (0, 0, 0)), 30)
        elif self.state == "Pause":
            self.text.print_text(self.screen, (550, 775), [str(self.ship.bullets)], ((255, 255, 255), (0, 0, 0)))
            self.text.print_text(self.screen, (50, 775), [str(self.ship.points)], ((255, 255, 255), (0, 0, 0)))
            self.enemy.draw(self.screen)
            self.ship.draw_shouts(self.screen)
            self.ship.draw(self.screen)
            self.ship.draw_life(self.screen)
            self.explosions.draw(self.screen)
            self.text.print_text(self.screen, (300, 300), ["Pause"], ((255, 255, 0), (0, 0, 0)), 80)

        pygame.display.flip()

    def run(self):
        #main loop
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)


pygame.init()

game = Game()
game.run()

pygame.quit()
