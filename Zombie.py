#-*-coding:latin1-*-
'''
Created on 28/09/2015

@author: Guilherme Campiotto
'''
import pygame
from SpriteLists import enemy_list

from AssetsManager import Images
Images.init()

white = (255,255,255)

zombie1_image_orig = Images.get("Sprites/Zumbi1.png")#pygame.image.load("Images\Sprites\Zumbi.jpg")
zombie1_image = pygame.transform.scale(zombie1_image_orig, (200, 102))

zombie2_orig = Images.get("Sprites/Zumbi2.png")
zombie2_image = pygame.transform.scale(zombie2_orig, (200, 102))

zombie3_orig = Images.get("Sprites/Zumbi3.png")
zombie3_image = pygame.transform.scale(zombie3_orig, (200, 102))

zombie4_orig = Images.get("Sprites/Zumbi4.png")
zombie4_image = pygame.transform.scale(zombie4_orig, (200, 102))

zombie_dying_orig = Images.get("Sprites/Zumbi_morrendo.png")
zombie_dying_image = pygame.transform.scale(zombie_dying_orig, (720, 100))

zombie1_frames = []
zombie2_frames = []
zombie3_frames = []
zombie4_frames = []
zombie_dying_frames = []

zombie_frame_height = 102
zombie_frame_width = 66

# Adicionando os sprites dos zumbis em listas.
for distance in range(3):
    frame_pos_x = zombie_frame_width * distance
    
    frame_zombie1 = zombie1_image.subsurface((frame_pos_x, 0), (zombie_frame_width, zombie_frame_height) )
    zombie1_frames.append(frame_zombie1)
    
    frame_zombie2 = zombie2_image.subsurface((frame_pos_x, 0), (zombie_frame_width, zombie_frame_height) )
    zombie2_frames.append(frame_zombie2)
    
    frame_zombie3 = zombie3_image.subsurface((frame_pos_x, 0), (zombie_frame_width, zombie_frame_height) )
    zombie3_frames.append(frame_zombie3)
    
    frame_zombie4 = zombie4_image.subsurface((frame_pos_x, 0), (zombie_frame_width, zombie_frame_height) )
    zombie4_frames.append(frame_zombie4)

zombie_dying_frame_height = 100
zombie_dying_frame_width = 72

for distance in range(10):
    frame_pos_x = zombie_dying_frame_width * distance
    frame_zombie_dying = zombie_dying_image.subsurface((frame_pos_x, 0), (zombie_dying_frame_width, zombie_dying_frame_height) )
    zombie_dying_frames.append(frame_zombie_dying)


class Zombie(pygame.sprite.Sprite):
    
    def __init__(self, hp, damage, speed, zombie_frames):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.zombie_frames = zombie_frames
        self.zombie_dying_frames = zombie_dying_frames
        self.alive = True
        self.can_change_sprite = True
        self.image = self.zombie_frames[self.index]
        self.rect = self.image.get_rect()
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.can_remove = False
    
    def move(self, barricade_resistance):
        # Animação do inimigo
        if self.hp > 0:
            if self.can_change_sprite: # Aumenta o tempo entre cada frame.
                self.can_change_sprite = False
                if self.index < 3:
                    self.image = self.zombie_frames[self.index]
                    self.index +=1
                else:
                    self.index = 0
                    self.image = self.zombie_frames[self.index]
            else:
                self.can_change_sprite = True
            # Movimento
            self.rect.x -= self.speed
            if barricade_resistance > 0:
                if self.rect.x < 290:
                    self. rect.x = 290
        else:
            #Animação do zumbi morrendo
            self.alive = False
            if self.can_change_sprite:
                self.can_change_sprite = False
                if self.index < 10:
                    self.image = self.zombie_dying_frames[self.index]
                    self.index +=1
                else:
                    self.can_remove = True
            else:
                self.can_change_sprite = True
def move_zombies(barricade_resistance):
    for enemy in enemy_list:
        enemy.move(barricade_resistance)
