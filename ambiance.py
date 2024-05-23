import pygame
from random import randint


class MaxSizeList(object):

    def __init__(self, max_length):
        self.max_length = max_length
        self.ls = []

    def push(self, st):
        if len(self.ls) == self.max_length:
            del self.ls[0]
            self.ls.pop(0)
        self.ls.append(st)

    def get_list(self):
        return self.ls




class Cloud():

	def __init__(self, vel, pos, img):
		self.vel = vel
		self.pos = pos 
		self.img = img
		self.passed = False
	def draw(self, screen):
		if self.pos[0] > 1380:
			self.passed = True
		self.pos = (self.pos[0] + self.vel/10, self.pos[1])
		screen.blit(self.img, self.pos)


class Clouds():

	clouds = MaxSizeList(10)

	def __init__(self,cloudImages):
		self.cloudImages = cloudImages
		for x in range(0,10):
			self.add(Cloud(randint(1, 3), (randint(-100, 1380), randint(100, 620)), self.cloudImages[randint(0, len(self.cloudImages)-1)]))

	def add(self, cloud):
		Clouds.clouds.push(cloud)

	def draw(self, screen):
		cloudsList = Clouds.clouds.get_list()
		for x in range(0, len(cloudsList)):
			if cloudsList[x].passed:
				cloudsList.pop(x)
				self.add(Cloud(randint(1, 3), (randint(-200, -180), randint(100, 620)), self.cloudImages[randint(0, len(self.cloudImages)-1)]))
			cloudsList[x].draw(screen)