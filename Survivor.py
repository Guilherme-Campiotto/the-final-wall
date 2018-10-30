#-*-coding:latin1-*-
'''
Created on 14/09/2015

@author: Guilherme Campiotto
'''
import pygame
from pygame.constants import K_w, K_s, K_d, K_a, K_f, QUIT, KEYUP, K_SPACE, K_r, USEREVENT, K_ESCAPE
from SpriteLists import all_sprites_list, bullet_list
from Menus import Pause

from AssetsManager import Images

pygame.mixer.init()
Images.init()

# Controles
up = K_w
down = K_s
left = K_a
right = K_d
shoot = K_SPACE
reload_b = K_r
change_weapon = K_f
pause = K_ESCAPE

# Eventos
shoot_interval_event = USEREVENT
reload_event = USEREVENT+1

white = (255,255,255)

survivor_pistol_image = Images.get("Sprites/Sobrevivente_parado_pistola.png")
survivor_walking_pistol_image = Images.get("Sprites/Sobrevivente_andando_pistola.png")

survivor_revolver_image = Images.get("Sprites/Sobrevivente_parado_revolver.png")
survivor_walking_revolver_image = Images.get("Sprites/Sobrevivente_andando_revolver.png")

survivor_ak_47_image = Images.get("Sprites/Sobrevivente_parado_ak47.png")
survivor_walking_ak_47_image = Images.get("Sprites/Sobrevivente_andando_ak47.png")

survivor_sniper_rifle_image = Images.get("Sprites/Sobrevivente_parado_sniper.png")
survivor_walking_sniper_rifle_image = Images.get("Sprites/Sobrevivente_andando_sniper.png")

bullet_image_orig = Images.get("Sprites/TiroPistola.jpg")
bullet_image = pygame.transform.scale(bullet_image_orig, (10, 2))

#pistol_sound = Sounds.get("Effects/Pistola_tiro.wav")
#revolver_sound = Sounds.get("Effects/Revolver_tiro.wav")
#ak_47_sound = Sounds.get("Effects/Ak47_tiro.wav")
#sniper_rifle_sound = Sounds.get("Effects/Sniper_tiro.wav")

pistol_sound = pygame.mixer.Sound("Sounds\Effects\Pistola_tiro.wav")
revolver_sound = pygame.mixer.Sound("Sounds\Effects\Revolver_tiro.wav")
ak_47_sound = pygame.mixer.Sound("Sounds\Effects\Ak47_tiro.wav")
sniper_rifle_sound = pygame.mixer.Sound("Sounds\Effects\Sniper_tiro.wav")

pistol_reload_sound = pygame.mixer.Sound("Sounds\Effects\Pistola_recarregando.wav")
revolver_reload_sound = pygame.mixer.Sound("Sounds\Effects\Revolver_recarregando.wav")
ak_47_reload_sound = pygame.mixer.Sound("Sounds\Effects\Ak47_recarregando.wav")
sniper_rifle_reload_sound = pygame.mixer.Sound("Sounds\Effects\Sniper_recarregando.wav")

pygame.init()

pause_screen = Pause()

# Dimensões da animação da pistola e do revolver.
survivor_frame_height = 122
survivor_frame_width = 72

# Dimensões da animação da ak_47.
survivor_frame_height_2 = 117
survivor_frame_width_2 = 88

# Dimensões da animação da sniper.

survivor_frame_height_3 = 117
survivor_frame_width_3 = 87

survivor_walking_frames_pistol = []
survivor_walking_frames_revolver = []
survivor_walking_frames_sniper_rifle = []
survivor_walking_frames_ak_47 = []

# Adiciona todas as animações do personagem em listas, cada lista de uma arma.
for distance in range(8):
    frame_pos_x1 = survivor_frame_width * distance # Posição para selecionar o frame da pistola e do revolver.
    frame_pos_x2 = survivor_frame_width_2 * distance # Posição para selecionar o frame da ak_47.
    frame_pos_x3 = survivor_frame_width_3 * distance # Posição para selecionar o frame da sniper.
    
    survivor_frame_pistol = survivor_walking_pistol_image.subsurface((frame_pos_x1, 0), (survivor_frame_width, survivor_frame_height) )
    survivor_frame_revolver = survivor_walking_revolver_image.subsurface((frame_pos_x1, 0), (survivor_frame_width, survivor_frame_height) )
    survivor_frame_ak_47 = survivor_walking_ak_47_image.subsurface((frame_pos_x2, 0), (survivor_frame_width_2, survivor_frame_height_2) )
    survivor_frame_sniper_rifle = survivor_walking_sniper_rifle_image.subsurface((frame_pos_x3, 0), (survivor_frame_width_3, survivor_frame_height_3) )
    
    survivor_walking_frames_pistol.append(survivor_frame_pistol)
    survivor_walking_frames_revolver.append(survivor_frame_revolver)
    survivor_walking_frames_ak_47.append(survivor_frame_ak_47)
    survivor_walking_frames_sniper_rifle.append(survivor_frame_sniper_rifle)

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, damage, pierce):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.damage = damage
        self.pierce = pierce
        
    def update(self):
        self.rect.x += 50
        
        
class Weapon(pygame.sprite.Sprite):
    
    def __init__(self, name, image_walking, image_still, bullets, reload_time, shoot_interval, damage, pierce, available, bullet_distance_x, bullet_distance_y, shoot_sound, reload_sound):
        self.name = name
        self.image_walking = image_walking
        self.image_still = image_still
        self.available = available
        self.inicial_bullets = bullets
        self.bullets = bullets
        self.reload_time = reload_time
        self.can_shoot = True
        self.shoot_interval = shoot_interval
        self.damage = damage
        self.pierce = pierce
        self.bullet_distance_x = bullet_distance_x
        self.bullet_distance_y = bullet_distance_y
        self.shoot_sound = shoot_sound
        self.reload_sound = reload_sound
    def reload(self):
        self.reload_sound.play()
        pygame.time.set_timer(reload_event, self.reload_time)
    def shoot(self, x_position, y_position, weapon):
        self.shoot_sound.play()
        self.can_shoot = False
        self.bullets -= 1
        weapon_bullet = Bullet(weapon.damage, weapon.pierce)
        pygame.time.set_timer(shoot_interval_event, self.shoot_interval)
        weapon_bullet.rect.x = x_position + self.bullet_distance_x
        weapon_bullet.rect.y = y_position + self.bullet_distance_y
        all_sprites_list.add(weapon_bullet)
        bullet_list.add(weapon_bullet)
    
def remove_bullets():
        for bullet in bullet_list:
            if bullet.rect.x > 1000:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)


class Survivor(object):

    def __init__(self, x_position, y_position, primary_weapon, secondary_weapon, screen):
        self.index = 0
        self.Vx = 0
        self.Vy = 0
        self.x = x_position
        self.y = y_position
        self.wait_reload = False
        self.can_change_weapon = True
        self.primary_weapon = primary_weapon
        self.current_weapon = primary_weapon
        
        self.walking_frames = self.current_weapon.image_walking
        self.image_still = self.current_weapon.image_still
        self.image = self.image_still
        self.rect = self.image.get_rect()
        
        self.secondary_weapon = secondary_weapon
        self.screen = screen
        
    # Controle do personagem
    def controls(self):
        # Anda
        if pygame.key.get_pressed()[right]:
            self.Vx = 10
        if pygame.key.get_pressed()[left]:
            self.Vx = -10
        if pygame.key.get_pressed()[up]:
            self.Vy = -10
        if pygame.key.get_pressed()[down]:
            self.Vy = 10
            
        # Atira com a arma.
        if (pygame.key.get_pressed()[shoot]) and not self.wait_reload:
            if self.current_weapon.can_shoot and self.current_weapon.bullets > 0:
                self.current_weapon.shoot(self.x, self.y, self.current_weapon)
            
            # Recarrega sozinho se a arma estiver sem balas.
            elif self.current_weapon.bullets == 0:
                self.current_weapon.reload() # Recarrega
                self.wait_reload = True # Espera terminar de carregar.   
        
        # Recarrega a arma atual pressionando o botão.
        if (pygame.key.get_pressed()[reload_b]) and not self.wait_reload and self.current_weapon.bullets < self.current_weapon.inicial_bullets:
            self.current_weapon.bullets = 0
            self.current_weapon.reload()
            self.wait_reload = True # Espera terminar de carregar.
        
        # Troca de arma.
        if (pygame.key.get_pressed()[change_weapon]) and self.can_change_weapon:
            self.can_change_weapon = False
            if self.current_weapon == self.primary_weapon:
                self.current_weapon = self.secondary_weapon
                self.walking_frames = self.current_weapon.image_walking
            else:
                self.current_weapon = self.primary_weapon
                self.walking_frames = self.current_weapon.image_walking
        
        # Pausa o jogo.
        if (pygame.key.get_pressed()[pause]):
            pause_screen.draw(self.screen)
            
        for e in pygame.event.get():
            if (e.type == QUIT):
                exit()
            if (e.type == shoot_interval_event):
                self.current_weapon.can_shoot = True
            if (e.type == reload_event and self.wait_reload):
                self.current_weapon.bullets = self.current_weapon.inicial_bullets
                self.wait_reload = False
            if (e.type == KEYUP):
                if (e.key == change_weapon):
                    self.can_change_weapon = True 
                if (e.key == right):
                    self.Vx = 0
                elif (e.key == left):
                    self.Vx = 0
                if (e.key == up):
                    self.Vy = 0
                elif (e.key == down):
                    self.Vy = 0
                    
    # Movimentação e limite de movimento
    def ajust_position(self):
        # Animação andando.
        if self.index < 8:
            self.image = self.walking_frames[self.index]
            self.index += 1
        else:
            self.index = 0
            self.image = self.walking_frames[self.index]
        if self.x > 190:
            self.x = 190
        if self.x < 0:
            self.x = 0
        if self.y > 450:
            self.y = 450
        if self.y < 200:
            self.y = 200
        self.x += self.Vx
        self.y += self.Vy
        if self.Vx == 0 and self.Vy == 0:
            self.image = self.current_weapon.image_still 
            
    # Recarrega armas após concluir fase.
    def auto_reload(self): 
        self.primary_weapon.bullets = self.primary_weapon.inicial_bullets
        self.secondary_weapon.bullets = self.secondary_weapon.inicial_bullets
        
    # Equipa as armas selecionadas no personagem através da variavel do menu inventário que contem o nome da arma selecionada.
    def update_weapons(self, primary_name, secondary_name):
        if primary_name == "pistol":
            self.primary_weapon = weapons[0]
            self.current_weapon = weapons[0]
        elif primary_name == "revolver":
            self.primary_weapon = weapons[1]
            self.current_weapon = weapons[1]
        elif primary_name == "ak_47":
            self.primary_weapon = weapons[2]
            self.current_weapon = weapons[2]
        elif primary_name == "sniper_rifle":
            self.primary_weapon = weapons[3]
            self.current_weapon = weapons[3]   
                            
        if secondary_name == "pistol":
            self.secondary_weapon = weapons[0]
        elif secondary_name == "revolver":
            self.secondary_weapon = weapons[1]
        elif secondary_name == "ak_47":
            self.secondary_weapon = weapons[2]
        elif secondary_name == "sniper_rifle":
            self.secondary_weapon = weapons[3]
            
        # Arruma a animação com a arma certa.
        self.walking_frames = self.current_weapon.image_walking
        self.image_still = self.current_weapon.image_still
            
" Armas do jogo."
"                     nome,        , animação andando,                     imagem parada,                balas, tempo de reload, intervalo de tiros, dano da arma, tiros perfuram, arma disponivel,  posição x da bala, posição y da bala, som do tiro,        som da arma recarregando."
pistol = Weapon(      "Pistola",     survivor_walking_frames_pistol,       survivor_pistol_image,        18,    2000,            150,                3,            False,          True,             30,                10,                pistol_sound,       pistol_reload_sound) 
revolver = Weapon(    "Revolver",    survivor_walking_frames_revolver,     survivor_revolver_image,      8,     3000,            300,                5,            False,          False,            30,                15,                revolver_sound,     revolver_reload_sound)
ak_47 = Weapon(       "AK-47",       survivor_walking_frames_ak_47,        survivor_ak_47_image,         30,    3000,            80,                 4,            False,          False,            45,                20,                ak_47_sound,        ak_47_reload_sound)
sniper_rifle = Weapon("Sniper Rifle",survivor_walking_frames_sniper_rifle, survivor_sniper_rifle_image,  5,     4000,            400,                7,            True,           False,            40,                13,                sniper_rifle_sound, sniper_rifle_reload_sound)

weapons = []
weapons.append(pistol)
weapons.append(revolver)
weapons.append(ak_47)
weapons.append(sniper_rifle)