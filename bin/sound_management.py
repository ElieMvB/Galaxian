import pygame


class SoundManagement:
    def __init__(self):
        #every sound is accessible from this dictionary
        self.sounds = {
            "ship_laser_blast": pygame.mixer.Sound("assets/sounds/ship/laser_blast.ogg"),
            "explosion": pygame.mixer.Sound("assets/sounds/ship/explosion.ogg"),
            "recharging": pygame.mixer.Sound("assets/sounds/ship/recharging.ogg"),
            "enemy_laser_blast0": pygame.mixer.Sound("assets/sounds/enemy/laser_blast0.ogg"),
            "enemy_laser_blast1": pygame.mixer.Sound("assets/sounds/enemy/laser_blast1.ogg"),
            "enemy_laser_blast2": pygame.mixer.Sound("assets/sounds/enemy/laser_blast2.ogg"),
            "enemy_explosion": pygame.mixer.Sound("assets/sounds/enemy/explosion.ogg"),
            "dong": pygame.mixer.Sound("assets/sounds/enemy/dong.ogg"),
            "Musics": [pygame.mixer.Sound("assets/sounds/back_ground/Soul_Knight_OST_Forest.ogg"),
                       pygame.mixer.Sound("assets/sounds/back_ground/Undertale_Megalovania.ogg"),
                       pygame.mixer.Sound("assets/sounds/back_ground/MegaMan_2.ogg"),
                       pygame.mixer.Sound("assets/sounds/back_ground/X-MEN_2 _Clone_Wars_Magnetos Quarters.ogg")]
        }

        #initialisation of the channels
        self.channels = [pygame.mixer.Channel(i) for i in range(8)]

        #every channel has its own use
        #two of them are used for enemy blast because enemies blast two lasers at the same time
        self.channels[1].set_volume(0.8) #ship blast and recharging
        self.channels[2].set_volume(0.9) #ship explosion
        self.channels[3].set_volume(0.5) #enemy blast
        self.channels[4].set_volume(0.5) #enemy blast
        self.channels[5].set_volume(0.7) #enemy explosion
        self.channels[6].set_volume(0.75) #dif up
        self.channels[7].set_volume(0.8) #music

    def play(self, key, c=0):
        if c == 3:
            if self.channels[3].get_busy():
                c = 4
        self.channels[c].play(self.sounds[key])

    def stop(self, c):
        self.channels[c].stop()
