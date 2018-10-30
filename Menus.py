#-*-coding:latin1-*-
'''
Created on 17/10/2015

@author: Guilherme Campiotto
'''

import pygame
from pygame import MOUSEBUTTONUP
from AssetsManager import Fonts, Images
from SpriteLists import all_sprites_list, enemy_list, bullet_list
from DiaryPages import diary

Fonts.init()
Images.init()
pygame.mixer.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 255, 0)
light_green = (0, 200, 0)
papaya_whip = (255, 239, 213)
bisque_2 = (238, 213, 183)
moccasin = (255, 228, 181)
orange = (255, 165, 0)
orange_red = (255, 69, 0)
firebrick = (178, 34, 34)

menu_music = pygame.mixer.Sound("Sounds\Musics\Menu_musica.wav")
helicopter_sound = pygame.mixer.Sound("Sounds\Effects\helicoptero.wav")

screen_pause_original = Images.get("background_pausa.png")
screen_pause = pygame.transform.scale(screen_pause_original, (1000, 600))
background_menu_orig = Images.get("background_menu.jpg")
background_menu_image = pygame.transform.scale(background_menu_orig, (1000, 600))
background_next_day_orig = Images.get("Background_fase_concluida.jpg")
background_next_day_image = pygame.transform.scale(background_next_day_orig, (1000, 600))
game_controls_original = Images.get("Controles.png")
game_controls = pygame.transform.scale(game_controls_original, (555, 157))

def text_objects(text, font, cor):
    "Retorna uma surface e o retângulo do tamanho da fonte"
    textSurface = font.render(text, True, cor)
    return textSurface, textSurface.get_rect()
    
class InicialMenu(object):
    def __init__(self):
        self.can_draw_menu = True
        self.can_draw_controls = True
        self.can_click = True
        
        self.title = Fonts.get("Menu/Zombie.ttf", 80)
        self.TextSurf, self.TextRect = text_objects("The Final Wall", self.title, red)
        self.TextRect.center = (500),(150)
        
        self.title2 = Fonts.get("Menu/Zombie.ttf", 50)
        self.TextSurf2, self.TextRect2 = text_objects("Controles", self.title, red)
        self.TextRect2.center = (500),(150)
        
        self.quit_game = False
        self.background = background_menu_image
        self.game_controls = game_controls
    def button(self, screen, message, font_size, x, y, width, height, inactive_color, active_color, action=None):
         
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()         
        
        if x + width > self.mouse[0] > x and y + height > self.mouse[1] > y :
            pygame.draw.rect(screen, inactive_color,(x,y,width,height))
             
            if self.click[0] == 1 and action == "start" and self.can_click:
                "Se o botão continuar for pressionado retorna ao jogo."
                self.can_click = False
                self.can_draw_menu = False
            if self.click[0] == 1 and action == "continue"  and self.can_click:
                self.can_click = False
                self.can_draw_controls = False
            if self.click[0] == 1 and action == "quit":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.quit_game = True
        else:
            pygame.draw.rect(screen, active_color,(x, y, width, height))  
            
        self.text = Fonts.get("Tela do jogo/Zombie.ttf", font_size)
        self.text_surf, self.text_rect = text_objects(message, self.text, black)
        self.text_rect.center = ( (x + (width / 2) ), (y + (height / 2) ) )
        screen.blit(self.text_surf, self.text_rect)
        
    def draw(self, screen):
        # Tela do menu principal.
        while self.can_draw_menu:
            screen.blit(self.background, (0, 0))
            screen.blit(self.TextSurf, self.TextRect)         
            self.button(screen, "Iniciar", 25, 430, 300, 130, 80, firebrick, red, "start")
            self.button(screen, "Sair", 25, 430, 450, 130, 80, firebrick, red, "quit") 
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.quit_game:
                    pygame.quit()
                    exit()
        # Tela dos controles.
        while self.can_draw_controls:
            screen.fill(black)
            screen.blit(self.TextSurf2, self.TextRect2)
            screen.blit(self.game_controls, (220, 200))
            self.button(screen, "Continuar", 20, 430, 380, 130, 50, firebrick, red, "continue")
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.can_click = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        
class NextDayScreen(pygame.sprite.Sprite):
    def __init__(self):
        self.hours = 8
        self.hours_wall = 0
        self.hours_weapons = 0
        self.can_draw = True
        self.can_click = True
        self.image = background_next_day_image
        self.menu_music = menu_music
        
        self.title = Fonts.get("Tela do jogo/Zombie.ttf", 50)
        self.TextSurf, self.TextRect = text_objects("Voce sobreviveu aos zumbis", self.title, red)
        self.TextRect.center = (500),(150)
        
        self.title_2 = Fonts.get("Tela do jogo/Zombie.ttf", 25)
        self.TextSurf_2, self.TextRect_2 = text_objects("Horas restantes ", self.title_2, red)
        self.TextRect_2.center = (450),(230)

        self.TextSurf_3, self.TextRect_3 = text_objects("Procurar armas ", self.title_2, red)
        self.TextRect_3.center = (450),(330)
        
        self.TextSurf_4, self.TextRect_4 = text_objects("Arrumar muro ", self.title_2, red)
        self.TextRect_4.center = (450),(430)
        
    def button(self, screen, message, font_size, x, y, width, height, inactive_color, active_color, action=None):
         
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()         
        
        if x + width > self.mouse[0] > x and y + height > self.mouse[1] > y :
            pygame.draw.rect(screen, inactive_color,(x,y,width,height))
             
            if self.click[0] == 1 and action == "unpause":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.can_draw = False
            if y == 305:
                if self.click[0] == 1 and action == "more" and self.can_click:
                    if self.hours > 0:
                        self.can_click = False
                        self.hours -= 1
                        self.hours_weapons += 1
                         
                if self.click[0] == 1 and action == "less" and self.can_click:
                    if self.hours_weapons > 0:
                        self.can_click = False
                        self.hours += 1
                        self.hours_weapons -= 1  
         
            if y == 405:
                if self.click[0] == 1 and action == "more" and self.can_click:
                    if self.hours > 0:
                        self.can_click = False
                        self.hours -= 1
                        self.hours_wall += 1   
                         
                if self.click[0] == 1 and action == "less" and self.can_click:
                    if self.hours_wall > 0:
                        self.can_click = False
                        self.hours += 1
                        self.hours_wall -= 1  
        else:
            pygame.draw.rect(screen, active_color,(x, y, width, height))    
             
        self.text = Fonts.get("Tela do jogo/zombieCat.ttf", font_size)
        self.text_surf, self.text_rect = text_objects(message, self.text, black)
        self.text_rect.center = ( (x + (width / 2) ), (y + (height / 2) ) )
        screen.blit(self.text_surf, self.text_rect)         
        
    def draw(self, screen):
        # Tela de distribuir horas.
        while self.can_draw:
            screen.blit(self.image, (0, 0))
            screen.blit(self.TextSurf, self.TextRect)
            screen.blit(self.TextSurf_2, self.TextRect_2)
            screen.blit(self.TextSurf_3, self.TextRect_3)
            screen.blit(self.TextSurf_4, self.TextRect_4)    
             
            self.button(screen, str(self.hours), 15, 570, 205, 40, 40, papaya_whip, papaya_whip, None)
             
            self.button(screen, "-", 15, 570, 305, 40, 40, papaya_whip, bisque_2, "less")
            self.button(screen, str(self.hours_weapons), 15, 620, 305, 40, 40, papaya_whip, papaya_whip, None)
            self.button(screen, "+", 15, 670, 305, 40, 40, papaya_whip, bisque_2, "more")
                     
            self.button(screen, "-", 15, 570, 405, 40, 40, papaya_whip, bisque_2, "less")
            self.button(screen, str(self.hours_wall), 15, 620, 405, 40, 40, papaya_whip, papaya_whip, None)
            self.button(screen, "+", 15, 670, 405, 40, 40, papaya_whip, bisque_2, "more")        
             
            self.button(screen, "CONTINUAR", 15, 480, 480, 145, 50, green, light_green, "unpause")   
             
            pygame.display.update()
             
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.can_click = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    def reset(self):
        self.hours = 8
        self.hours_wall = 0
        self.hours_weapons = 0
        self.can_draw = True
        self.can_click = True
    
    def play_music(self):
        self.menu_music.play(-1)
    def stop_music(self):
        self.menu_music.stop()

class GameOver(object):
    
    def __init__(self):
        self.can_draw = True
        self.quit_game = False
        self.screen_color = red
        self.title = Fonts.get("Tela do jogo/Zombie.ttf", 50)
        self.TextSurf, self.TextRect = text_objects("Fim de jogo", self.title, black)
        self.TextRect.center = (500),(150)
    
    def reset_game(self):
        # Remove inimigos e tiros para reiniciar a fase.
        for enemy in enemy_list:
            enemy_list.remove(enemy)
            all_sprites_list.remove(enemy)
        for bullet in bullet_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    
    def button(self, screen, message, font_size, x, y, width, height, inactive_color, active_color, action=None):
         
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()         
        
        if x + width > self.mouse[0] > x and y + height > self.mouse[1] > y :
            pygame.draw.rect(screen, inactive_color,(x,y,width,height))
             
            if self.click[0] == 1 and action == "continue":
                self.reset_game()
                self.can_draw = False
            if self.click[0] == 1 and action == "quit":
                self.quit_game = True
        else:
            pygame.draw.rect(screen, active_color,(x, y, width, height))  
            
        self.text = Fonts.get("Tela do jogo/zombieCat.ttf", font_size)
        self.text_surf, self.text_rect = text_objects(message, self.text, black)
        self.text_rect.center = ( (x + (width / 2) ), (y + (height / 2) ) )
        screen.blit(self.text_surf, self.text_rect)

    def draw(self, screen):
        # Tela de Game Over.
        while self.can_draw:
            screen.fill(red)
            screen.blit(self.TextSurf, self.TextRect)
            
            self.button(screen, "CONTINUAR", 15, 350, 250, 145, 50, orange, orange_red, "continue")  
            self.button(screen, "SAIR", 15, 550, 250, 145, 50, orange, orange_red, "quit")
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.quit_game:
                    pygame.quit()
                    exit()
        self.can_draw = True

class Pause(object):
    
    def __init__(self):
        self.can_draw = True
        self.quit_game = False
        self.screen_color = black
        self.title = Fonts.get("Tela do jogo/Zombie.ttf", 50)
        self.game_controls = game_controls
        self.TextSurf, self.TextRect = text_objects("Pausa", self.title, black)
        self.TextRect.center = (490),(150)
        self.screen_pause = screen_pause
    
    def button(self, screen, message, font_size, x, y, width, height, inactive_color, active_color, action=None):
         
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()         
        
        if x + width > self.mouse[0] > x and y + height > self.mouse[1] > y :
            pygame.draw.rect(screen, inactive_color,(x,y,width,height))
             
            if self.click[0] == 1 and action == "continue":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.can_draw = False
            if self.click[0] == 1 and action == "quit":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.quit_game = True
        else:
            pygame.draw.rect(screen, active_color,(x, y, width, height))  
            
        self.text = Fonts.get("Tela do jogo/zombieCat.ttf", font_size)
        self.text_surf, self.text_rect = text_objects(message, self.text, black)
        self.text_rect.center = ( (x + (width / 2) ), (y + (height / 2) ) )
        screen.blit(self.text_surf, self.text_rect)
        
    
    def draw(self, screen):
        while self.can_draw:
            screen.blit(self.game_controls, (220, 320))
            screen.blit(self.screen_pause, (0,0))
            screen.blit(self.TextSurf, self.TextRect)
            
            self.button(screen, "CONTINUAR", 15, 320, 230, 145, 50, orange, orange_red, "continue")  
            self.button(screen, "SAIR", 15, 520, 230, 145, 50, orange, orange_red, "quit")
            
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.quit_game:
                    pygame.quit()
                    exit()
        self.can_draw = True      

class InventoryMenu(object):
    def __init__(self):
        self.diary = diary
        self.page_day = 0
        self.image = background_next_day_image
        self.inventory_image = Images.get("Inventario.png")
        self.show_diary_page = False
        self.pistol_icon = Images.get("Pistola_icone.png")
        self.revolver_icon = Images.get("Revolver_icone.png")
        self.ak_47_icon = Images.get("Ak_47_icone.png")
        self.sniper_icon = Images.get("Sniper_icone.png")
        self.locked_icon = Images.get("Trava_icone.png")
        self.slot_1_icon = self.pistol_icon
        self.slot_2_icon = self.revolver_icon
        self.slot_3_icon = self.ak_47_icon
        self.slot_4_icon = self.sniper_icon
        
        self.primary_weapon_icon = self.pistol_icon
        self.secondary_weapon_icon = self.pistol_icon
        
        self.can_click = True
        self.can_draw = True
        self.select_weapon = 1
        self.weapon_1_name = "Pistol"
        self.weapon_2_name = "Pistol"
        
        self.position_selected_1 = (530, 130)
        self.position_selected_2 = (700, 130)
        
        self.pistol_position_inventory = (165, 130)
        self.revolver_position_inventory = (335, 130)
        self.ak_47_position_inventory = (165, 265)
        self.sniper_rifle_position_inventory = (335, 265)
        
        self.pistol_selected_slot_1 = True
        self.pistol_selected_slot_1 = True
        self.revolver_selected = True
        self.pistol_selected = True
        self.pistol_selected = True
        
    def button(self, screen, message, font_size, x, y, width, height, inactive_color, active_color, action, transparent, weapon_name, weapons):
         
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()         
        
        if x + width > self.mouse[0] > x and y + height > self.mouse[1] > y :
            if not transparent:
                pygame.draw.rect(screen, inactive_color,(x,y,width,height))
             
            if self.click[0] == 1 and action == "continue":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.can_draw = False
              
            # Mostra pagina do diário.   
            elif self.click[0] == 1 and action == "show_page":
                if not self.show_diary_page:
                    self.show_diary_page = True
                else:
                    self.show_diary_page = False 
                    
            # Muda os icones das armas conforme selecionado.
            elif self.click[0] == 1 and action == "change_weapon" and self.can_click:
                self.can_click = False
                if self.select_weapon == 1:
                    self.select_weapon = 2
                    if weapon_name == "pistol":
                        self.weapon_1_name = "pistol"
                        self.primary_weapon_icon = self.pistol_icon
                    if weapon_name == "revolver" and weapons[1].available:
                        self.weapon_1_name = "revolver"
                        self.primary_weapon_icon = self.revolver_icon
                    if weapon_name == "ak_47" and weapons[2].available:
                        self.weapon_1_name = "ak_47"
                        self.primary_weapon_icon = self.ak_47_icon
                    if weapon_name == "sniper_rifle" and weapons[3].available:
                        self.weapon_1_name = "sniper_rifle"
                        self.primary_weapon_icon = self.sniper_icon               
                else:
                    self.select_weapon = 1
                    if weapon_name == "pistol":
                        self.weapon_2_name = "pistol"
                        self.secondary_weapon_icon = self.pistol_icon
                    if weapon_name == "revolver" and weapons[1].available:
                        self.weapon_2_name = "revolver"
                        self.secondary_weapon_icon = self.revolver_icon
                    if weapon_name == "ak_47" and weapons[2].available:
                        self.weapon_2_name = "ak_47"
                        self.secondary_weapon_icon = self.ak_47_icon
                    if weapon_name == "sniper_rifle" and weapons[3].available:
                        self.weapon_2_name = "sniper_rifle"
                        self.secondary_weapon_icon = self.sniper_icon
        elif not transparent:
            pygame.draw.rect(screen, active_color,(x, y, width, height))  
            
        self.text = Fonts.get("Tela do jogo/zombieCat.ttf", font_size)
        self.text_surf, self.text_rect = text_objects(message, self.text, black)
        self.text_rect.center = ( (x + (width / 2) ), (y + (height / 2) ) )
        screen.blit(self.text_surf, self.text_rect)
    
    def update(self):
        if self.page_day < 8:
            self.page_day += 1
        self.can_draw = True
      
    def run(self, screen, weapons):
        
        if weapons[1].available:
            self.slot_2_icon = self.revolver_icon
        else:
            self.slot_2_icon = self.locked_icon
            
        if weapons[2].available:
            self.slot_3_icon = self.ak_47_icon
        else:
            self.slot_3_icon = self.locked_icon
    
        if weapons[3].available:
            self.slot_4_icon = self.sniper_icon
        else:
            self.slot_4_icon = self.locked_icon        
                
        
        while self.can_draw:
            screen.fill(black)
            screen.blit(self.image, (0, 0))
            if not self.show_diary_page:    
                screen.blit(self.inventory_image, (130, 100)) 
                
                # Icones do inventário
                screen.blit(self.slot_1_icon, self.pistol_position_inventory)
                screen.blit(self.slot_2_icon, self.revolver_position_inventory)
                screen.blit(self.slot_3_icon, self.ak_47_position_inventory)
                screen.blit(self.slot_4_icon, self.sniper_rifle_position_inventory)
                screen.blit(self.primary_weapon_icon, self.position_selected_1)
                screen.blit(self.secondary_weapon_icon, self.position_selected_2)
                
                # Botões transparentes para selecionar armas.
                self.button(screen, "", 15, 165, 130, 130, 100, papaya_whip, moccasin, "change_weapon", True, "pistol", weapons)
                self.button(screen, "", 15, 335, 130, 130, 100, papaya_whip, moccasin, "change_weapon", True, "revolver", weapons)
                self.button(screen, "", 15, 165, 265, 130, 100, papaya_whip, moccasin, "change_weapon", True, "ak_47", weapons)
                self.button(screen, "", 15, 335, 265, 130, 100, papaya_whip, moccasin, "change_weapon", True, "sniper_rifle", weapons)
                
                
                # Botão para continuar o jogo e um botão transparente para acessar o diário.
                self.button(screen, "Continuar", 15, 690, 260, 130, 100, white, moccasin, "continue", False, None, None)
                self.button(screen, "", 15, 520, 260, 130, 100, papaya_whip, moccasin, "show_page", True, None, None)
            
            else:
                screen.blit(self.diary[self.page_day], (150, 80))
                self.button(screen, " X ", 25, 810, 510, 50, 50, papaya_whip, moccasin, "show_page", True, None, None)
                
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                        self.can_click = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
class GameFinished(object):
    def __init__(self):
        self.can_draw = True
        self.quit_game = False
        self.screen_color = black
        self.title = Fonts.get("Tela do jogo/Zombie.ttf", 50)
        self.game_controls = game_controls
        self.TextSurf, self.TextRect = text_objects("Fim de jogo", self.title, black)
        self.TextRect.center = (490),(150)
        self.helicopter_sound = helicopter_sound
    def play_sound(self):
        self.helicopter_sound.play()
        
    def button(self, screen, message, font_size, x, y, width, height, inactive_color, active_color, action=None):
         
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()         
        
        if x + width > self.mouse[0] > x and y + height > self.mouse[1] > y :
            pygame.draw.rect(screen, inactive_color,(x,y,width,height))
             
            if self.click[0] == 1 and action == "continue":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.reset_game()
                self.can_draw = False
            if self.click[0] == 1 and action == "quit":
                "Se o botão continuar for pressionado retorna ao jogo."
                self.quit_game = True
        else:
            pygame.draw.rect(screen, active_color,(x, y, width, height))  
            
        self.text = Fonts.get("Tela do jogo/zombieCat.ttf", font_size)
        self.text_surf, self.text_rect = text_objects(message, self.text, black)
        self.text_rect.center = ( (x + (width / 2) ), (y + (height / 2) ) )
        screen.blit(self.text_surf, self.text_rect)

    def run(self, screen):
        while self.can_draw:
            screen.fill(red)
            screen.blit(self.TextSurf, self.TextRect)
            
            self.button(screen, "SAIR", 15, 420, 230, 145, 50, orange, orange_red, "quit")
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.quit_game:
                    pygame.quit()
                    exit()