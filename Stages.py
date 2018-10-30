'''
Created on 09/10/2015

@author: Guilherme Campiotto
'''
from random import choice
from SpriteLists import all_sprites_list, enemy_list
from Zombie import Zombie, zombie1_frames, zombie2_frames, zombie3_frames, zombie4_frames

zombie_position_y = [200,250,300,350,400,450]
zombie_position_x = [200,250,300,350,400,450]

zombie_types = [zombie1_frames, zombie2_frames, zombie3_frames, zombie4_frames]

stage_1 = []
stage_2 = []
stage_3 = []
stage_4 = []
stage_5 = []
stage_6 = []
stage_7 = []
stage_8 = []
stage_9 = []
stage_10 = []


all_stages = []

def zombie_respawn(zombie_type, zombies_number, distance):
    for i in range(zombies_number):
        zombie_position_h = choice(zombie_position_y)
        zombie_position_w = choice(zombie_position_x)
        if zombie_type == "weak_slow":
            zombie_weak = Zombie(5, 5, 6, choice(zombie_types)) # HP, dano, velocidade
            zombie_weak.rect.x = zombie_position_w + distance
            zombie_weak.rect.y = zombie_position_h
            all_sprites_list.add(zombie_weak)
            enemy_list.add(zombie_weak)
        if zombie_type == "weak_fast":
            zombie_weak = Zombie(5, 5, 7, choice(zombie_types))
            zombie_weak.rect.x = zombie_position_w + distance
            zombie_weak.rect.y = zombie_position_h
            all_sprites_list.add(zombie_weak)
            enemy_list.add(zombie_weak)        
        if zombie_type == "medium_slow":
            zombie_medium = Zombie(7, 7, 6, choice(zombie_types))
            zombie_medium.rect.x = zombie_position_w + distance
            zombie_medium.rect.y = zombie_position_h
            all_sprites_list.add(zombie_medium)
            enemy_list.add(zombie_medium)
        if zombie_type == "medium_fast":
            zombie_medium = Zombie(7, 7, 7, choice(zombie_types))
            zombie_medium.rect.x = zombie_position_w + distance
            zombie_medium.rect.y = zombie_position_h
            all_sprites_list.add(zombie_medium)
            enemy_list.add(zombie_medium)
        if zombie_type == "strong_slow":
            zombie_medium = Zombie(10, 10, 7, choice(zombie_types))
            zombie_medium.rect.x = zombie_position_w + distance
            zombie_medium.rect.y = zombie_position_h
            all_sprites_list.add(zombie_medium)
            enemy_list.add(zombie_medium)                        
        if zombie_type == "strong_fast":
            zombie_strong = Zombie(10, 10, 9, choice(zombie_types))  # testando um tipo de zumbi.
            zombie_strong.rect.x = zombie_position_w + distance
            zombie_strong.rect.y = zombie_position_h
            all_sprites_list.add(zombie_strong)
            enemy_list.add(zombie_strong)

class Stage(object):

    def __init__(self, zombie_type, zombies_number, distance, level):
        self.level = level
        self.zombie_type = zombie_type
        self.zombies_number = zombies_number
        self.distance = distance
    def run(self):
        zombie_respawn(self.zombie_type, self.zombies_number, self.distance)

def run_stage(stage):
    for stage_wave in stage:
        stage_wave.run()

stage_1_wave_1 = Stage("weak_slow", 9, 1000, 1)
stage_1_wave_2 = Stage("weak_fast", 7, 2000, 1)
stage_1_wave_3 = Stage("medium_slow", 9, 3000, 1)
stage_1.append(stage_1_wave_1)
stage_1.append(stage_1_wave_2)
stage_1.append(stage_1_wave_3) 

all_stages.append(stage_1)

stage_2_wave_1 = Stage("weak_slow", 9, 1000, 2)
stage_2_wave_2 = Stage("weak_fast", 8, 2000, 2)
stage_2_wave_3 = Stage("medium_slow", 9, 3000, 2)
stage_2.append(stage_2_wave_1)
stage_2.append(stage_2_wave_2)
stage_2.append(stage_2_wave_3) 

all_stages.append(stage_2)

stage_3_wave_1 = Stage("weak_slow", 11, 1000, 2)
stage_3_wave_2 = Stage("weak_fast", 10, 2000, 2)
stage_3_wave_3 = Stage("medium_slow", 12, 3000, 2)
stage_3.append(stage_3_wave_1)
stage_3.append(stage_3_wave_2)
stage_3.append(stage_3_wave_3) 

all_stages.append(stage_3)

stage_4_wave_1 = Stage("weak_fast", 7, 1000, 2)
stage_4_wave_2 = Stage("weak_fast", 11, 2000, 2)
stage_4_wave_3 = Stage("medium_slow", 13, 3000, 2)
stage_4.append(stage_4_wave_1)
stage_4.append(stage_4_wave_2)
stage_4.append(stage_4_wave_3) 

all_stages.append(stage_4)
        
stage_5_wave_1 = Stage("weak_fast", 10, 1000, 2)
stage_5_wave_2 = Stage("weak_fast", 10, 2000, 2)
stage_5_wave_3 = Stage("medium_slow", 10, 3000, 2)
stage_5.append(stage_5_wave_1)
stage_5.append(stage_5_wave_2)
stage_5.append(stage_5_wave_3) 

all_stages.append(stage_5) 

stage_6_wave_1 = Stage("weak_fast", 12, 1000, 2)
stage_6_wave_2 = Stage("medium_slow", 7, 2000, 2)
stage_6_wave_3 = Stage("medium_fast", 8, 3000, 2)
stage_6.append(stage_6_wave_1)
stage_6.append(stage_6_wave_2)
stage_6.append(stage_6_wave_3) 

all_stages.append(stage_6)    

stage_7_wave_1 = Stage("medium_slow", 10, 1000, 2)
stage_7_wave_2 = Stage("medium_slow", 7, 2000, 2)
stage_7_wave_3 = Stage("medium_slow", 8, 3000, 2)
stage_7.append(stage_7_wave_1)
stage_7.append(stage_7_wave_2)
stage_7.append(stage_7_wave_3) 

all_stages.append(stage_7)

stage_8_wave_1 = Stage("medium_fast", 10, 1000, 2)
stage_8_wave_2 = Stage("medium_slow", 10, 2000, 2)
stage_8_wave_3 = Stage("medium_slow", 9, 3000, 2)
stage_8.append(stage_8_wave_1)
stage_8.append(stage_8_wave_2)
stage_8.append(stage_8_wave_3) 

all_stages.append(stage_8)

stage_9_wave_1 = Stage("strong_slow", 8, 1000, 2)
stage_9_wave_2 = Stage("strong_slow", 9, 2000, 2)
stage_9_wave_3 = Stage("strong_slow", 9, 3000, 2)
stage_9.append(stage_9_wave_1)
stage_9.append(stage_9_wave_2)
stage_9.append(stage_9_wave_3) 

all_stages.append(stage_9)

stage_10_wave_1 = Stage("weak_fast", 30, 1000, 2)
stage_10_wave_2 = Stage("strong_slow", 14, 2000, 2)
stage_10_wave_3 = Stage("strong_fast", 11, 3000, 2)
stage_10.append(stage_10_wave_1)
stage_10.append(stage_10_wave_2)
stage_10.append(stage_10_wave_3) 

all_stages.append(stage_10)
        