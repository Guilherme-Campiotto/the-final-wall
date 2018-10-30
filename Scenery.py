#-*-coding:latin1-*-
'''
Created on 11/09/2015

@author: Guilherme Campiotto
'''
import pygame
from pygame.time import Clock

from AssetsManager import Images
from pygame.constants import FULLSCREEN

Images.init()
pygame.mixer.init()

stage_music = pygame.mixer.Sound("Sounds\Musics\Fase_musica.wav")

white = (255,255,255)

background_image = Images.get("militar_envir.jpg")
barricade_100_image_original = Images.get("Barricada100.png")
barricade_100_image = pygame.transform.scale(barricade_100_image_original,(550, 630))

barricade_70_image_original = Images.get("Barricada70.png")
barricade_70_image = pygame.transform.scale(barricade_70_image_original,(550, 630))

barricade_30_image_original = Images.get("Barricada30.png")
barricade_30_image = pygame.transform.scale(barricade_30_image_original,(550, 630))

barricade_0_image_original = Images.get("Barricada0.png")
barricade_0_image = pygame.transform.scale(barricade_0_image_original,(550, 630))


class Scenery(object):
    
    def __init__(self):
        self.size = (1000, 600)
        self.fps = 20
        self.clk = Clock()
        #self.screen = pygame.display.set_mode(self.size,FULLSCREEN, 32) # Fullscreen
        self.screen = pygame.display.set_mode(self.size) # Janela
        self.background = pygame.transform.scale(background_image,(self.size))
        self.music = stage_music
    def play_music(self):
        self.music.play(-1)
    def stop_music(self):
        self.music.fadeout(3000)

class Barricade(object):
    def __init__(self):
        self.resistance = 100
        self.stage_resistance = 100
        self.image_100 = barricade_100_image
        self.image_70 = barricade_70_image
        self.image_30 = barricade_30_image
        self.image_0 = barricade_0_image
        self.image = barricade_100_image
        self.x = 0
        self.y = 110
        
    def draw_barricade(self, screen):
        # Testa condições para mudar a imagem da barricada.
        if self.resistance <= 100 and self.resistance > 70:
            self.image = self.image_100
        elif self.resistance <= 70 and self.resistance > 30:
            self.image = self.image_70
        elif self.resistance <= 30 and self.resistance > 0:
            self.image = self.image_30
        elif self.resistance <= 0:
            self.image = self.image_0
        if self.resistance < 0:
            self.resistance = 0
        screen.blit(self.image, (self.x, self.y))
        
    def repair(self, hours):
        self.resistance += (hours * 5)
        if self.resistance > 100:
            self.resistance = 100
        self.stage_resistance = self.resistance
        
    def auto_repair(self):
        # Conserta novamente quando o jogo é reiniciado após o jogador perder.
        self.resistance = self.stage_resistance + 15 # Reinicia o jogo com o hp do muro no começo da fase um pouco maior.
        if self.resistance > 100:
            self.resistance = 100
        self.is_alive = True
