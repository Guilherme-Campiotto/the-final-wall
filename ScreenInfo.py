#-*-coding:latin1-*-
'''
Created on 05/10/2015

@author: Guilherme Campiotto
'''
import pygame
from AssetsManager import Fonts, Images
Fonts.init()
Images.init()

white = (255,255,255)
red = (200, 0, 0)

font_screen = Fonts.get("Tela do jogo/Zombie.ttf", 20)#pygame.font.Font("Fontes\Tela do jogo\Zombie.ttf", 20)
pause_icon_original = Images.get("Pausa.png")
pause_icon = pygame.transform.scale(pause_icon_original,(98, 56))

class ScreenInfo(object):

    def __init__(self):
        self.font = font_screen
        self.pause_icon = pause_icon
    
    def draw(self, screen, ammo, enemys_left, level, weapon_name, barricade_resistance):
        screen.blit(self.font.render( "Dia ", True, red), (50, 25))
        screen.blit(self.font.render( str(level), True, red), (150, 25))
        screen.blit(self.font.render( "Arma ", True, red), (50, 50))
        screen.blit(self.font.render( weapon_name, True, red), (150, 50))
        screen.blit(self.font.render( "Municao ", True, red), (50, 75))
        screen.blit(self.font.render( str(ammo), True, red), (150, 75))
        screen.blit(self.font.render( "Inimigos ", True, red), (50, 100))
        screen.blit(self.font.render( str(enemys_left), True, red), (150, 100))
        screen.blit(self.font.render( "Barricada ", True, red), (250,25))
        screen.blit(self.font.render( str(barricade_resistance), True, red), (380, 25))
        
        screen.blit(self.pause_icon, (850, 10))
