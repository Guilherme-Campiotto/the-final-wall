#-*-coding:latin1-*-
'''
Created on 30/09/2015

@author: Guilherme Campiotto
'''

from SpriteLists import all_sprites_list, enemy_list, bullet_list

def rectangle_dot(x,y, rect):
    if (x > rect.left) and (x <= rect.right) and (y >= rect.top) and (y <= rect.bottom):
        return True
    else:
        return False

def collision(rect1,rect2):
    for a,b in [(rect1,rect2),(rect2,rect1)]:
        if ((rectangle_dot(a.left, a.top, b)) or
            (rectangle_dot(a.left, a.bottom, b)) or
            (rectangle_dot(a.right, a.top, b)) or
            (rectangle_dot(a.right, a.bottom, b))):
                return True

def bullet_hit_detection():
    for enemy in enemy_list:
        if enemy.can_remove:
            enemy_list.remove(enemy)
            all_sprites_list.remove(enemy)
        for bullet in bullet_list:
            if collision(bullet.rect, enemy.rect):
                enemy.hp -= bullet.damage
                if  not bullet.pierce and enemy.alive:  # Tiros não atravessam se a arma não tiver bullet.pierce.
                    bullet_list.remove(bullet) 
                    all_sprites_list.remove(bullet)
                    break

def barricade_damage(barricade_resistance):
        count_damage = 0
        if barricade_resistance > 0:
            for enemy in enemy_list:
                if enemy.rect.x <= 450:
                    count_damage += 1
        return  count_damage
    
def character_hit_detection(survivor_rect):
    for enemy in enemy_list:
        if collision(enemy.rect, survivor_rect):
            # Game over
            pass
            