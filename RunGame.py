#-*-coding:latin1-*-
'''
Created on 11/09/2015

@author: Guilherme Campiotto
'''
import pygame
from Scenery import Scenery, Barricade
from Survivor import Survivor, remove_bullets
from SpriteLists import all_sprites_list, enemy_list
from Zombie import move_zombies
from CollisionDetection import bullet_hit_detection, barricade_damage
from ScreenInfo import ScreenInfo
from Stages import run_stage, all_stages
from DayGameplay import BeforeNextStage
from Menus import NextDayScreen, GameOver, InicialMenu, InventoryMenu, GameFinished
from Survivor import weapons
import thread
import time

black = (0, 0, 0)
character_position_x = 100
character_position_y = 200
start_time = time.time()
primary_weapon = weapons[0]
secondary_weapon = weapons[0]
current_day = 0
game_end = False

pygame.init()

# Objetos
scenery = Scenery()
barricade = Barricade()
survivor = Survivor(character_position_x,character_position_y, primary_weapon, secondary_weapon, scenery.screen)
screen_info = ScreenInfo()
before_next_stage = BeforeNextStage()
next_day_screen = NextDayScreen()
game_over = GameOver()
menu = InicialMenu()
inventory_menu = InventoryMenu()
game_finished = GameFinished()

# Menu do jogo.
menu.draw(scenery.screen)
thread.start_new_thread(run_stage, (all_stages[current_day],) )

scenery.play_music()

while (True):
    scenery.screen.fill(black)
    scenery.screen.blit(scenery.background,(0,0))
    barricade.draw_barricade(scenery.screen)
    scenery.screen.blit(survivor.image,(survivor.x,survivor.y))
    all_sprites_list.draw(scenery.screen)
    bullet_hit_detection()
    
    thread.start_new_thread(screen_info.draw, (scenery.screen, survivor.current_weapon.bullets, len(enemy_list), current_day + 1, survivor.current_weapon.name, barricade.resistance) )
    thread.start_new_thread(move_zombies, (barricade.resistance, ) )
    thread.start_new_thread(survivor.ajust_position, ( ) )
    
    
    elapsed_time  = time.time() - start_time
    
    if elapsed_time >= 2:
        start_time = time.time()
        barricade.resistance -= barricade_damage(barricade.resistance)
        
        if barricade.resistance == 0:
            # Para a música da fase.
            scenery.stop_music()
            
            # Mostra a tela de game over.
            game_over.draw(scenery.screen)
            
            # Retorna a música se o jogador quiser continuar.
            scenery.play_music()
            
            # Repara a barricada para o valor que estava no começo da fase.
            barricade.auto_repair()
            
            # Recarrega as armas automaticamente.
            survivor.auto_reload()
            
            # Gera os inimigos da fase atual novamente.
            run_stage(all_stages[current_day])
    
    survivor.controls()
    remove_bullets()
    
    scenery.clk.tick(scenery.fps)
    all_sprites_list.update()
    pygame.display.update()
    
    if len(enemy_list) == 0 and current_day < 9:
        # Para a música da fase e coloca um intervalo para aparecer a próxima tela.
        scenery.stop_music()
        before_next_stage.next_day_interval()
        
        if before_next_stage.can_advance:
            # Toca a música de menu .
            next_day_screen.play_music()
            before_next_stage.can_advance = False
            
            # Mostra o menu de distribuir horas.
            next_day_screen.draw(scenery.screen)
            
            # Procura armas.
            before_next_stage.search_weapons(next_day_screen.hours_weapons)
            
            # Arruma a barricada.
            barricade.repair(next_day_screen.hours_wall)
            
            # Arruma a screen das horas para a posição default.
            next_day_screen.reset()
            
            # Mostra o inventario e o diario.
            inventory_menu.run(scenery.screen, weapons)
            inventory_menu.update()
            
            # Equipa o personagem com as armas selecionadas no menu.
            survivor.update_weapons(inventory_menu.weapon_1_name, inventory_menu.weapon_2_name)
            
            if current_day < 9:
                # Para a música de menu e volta a tocar a música da fase.
                next_day_screen.stop_music()
                scenery.play_music()
                current_day += 1
                
                # Recarrega as armas equipadas.
                survivor.auto_reload()
                
                # Gera os inimigos para a proxima fase.
                thread.start_new_thread(run_stage, (all_stages[current_day], ) )
                
    elif len(enemy_list) == 0 and current_day == 9:
        # Toma o som final e aguarda 10 segundos.
        if not game_end:
            game_end = True
            start_time_final = time.time()
            scenery.stop_music()
            game_finished.play_sound()
        time_final = time.time() - start_time_final
                
        # Mostra a tela final do jogo.
        if time_final >= 10:
            game_finished.run(scenery.screen)
                