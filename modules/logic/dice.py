from random import randrange, random, lognormvariate
import pygame

class Dice():
    def __init__(self, sides, time, count):
        self.sides = sides
        self.value = 0
        self.rolling = False
        self.rollCount = 0
        self.throwCount = count
        self.time = time
        self.speed = None
    
    def get_value(self):
        return self.value
    
    def throw_dice(self):
        self.rolling = True
        self.rollCount = self.throwCount
        self.speed = self.random_number_list()

    def is_rolling(self):
        return self.rolling

    def roll(self):
        if(not self.rolling):
            return
        if(self.rollCount != self.throwCount):
            pygame.time.wait(self.speed.pop())
        self.rollCount-=1
        if(self.rollCount==0):
            self.rolling = False
        return self.random_number_dice_roll()

    def random_number_dice_roll(self):
        range = randrange(1, 100)
        incrementation = 1 + (range % (self.sides))
        self.value = incrementation 
        return incrementation
    
     # takes max value, and mult by random
    # returns in a list
    def random_number_list(self):
        d = list()
        for i in range(0, self.throwCount):
            d.append(int(self.time*random()))
        d.sort(reverse=True)
        return d