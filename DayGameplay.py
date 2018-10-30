#-*-coding:latin1-*-
'''
Created on 16/10/2015

@author: Guilherme Campiotto
'''

import time
import random

from Survivor import weapons

class BeforeNextStage(object):
    def __init__(self):
        self.hours = 12
        self.waiting = False
        self.can_advance = False
        self.unlock_next_weapon = 1
        self.chance = 0
    def next_day_interval(self):
        # Tempo para ir para a proxima fase.
        if not self.waiting:
            self.waiting = True
            self.start_time = time.time()
        self.current_time = time.time() - self.start_time
        if self.current_time >= 3:
            self.waiting = False
            self.can_advance = True
    def search_weapons(self, hours):
        # Calcula chance de encontrar uma nova arma.
        self.chance += (hours * 4)
        print "Chance de encontrar: " + str(self.chance) + "%"
        if random.randint(0, 100) < self.chance:
            self.chance = 0
            weapons[self.unlock_next_weapon].available = True
            print "achou uma nova arma: " + weapons[self.unlock_next_weapon].name
            if self.unlock_next_weapon <= 2:
                self.unlock_next_weapon +=1
        else:
            print "Não achou uma nova arma."
        