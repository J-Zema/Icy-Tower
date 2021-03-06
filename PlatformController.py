import pygame
import math
from random import randrange, random
from random import getrandbits
from Platform import Platform
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT, JUMP_VELOCITY, MAX_JUMP

# Inicjalizacja PyGame
pygame.init()

class PlatformController:
	"""Klasa odpwiedzialna za generowanie i rysowanie platform"""
	def __init__(self):
		self.platform_set = [] #tablica na platformy
		self.index = 10
		self.last_x = MAX_JUMP
		self.score = 0
		for i in range(0, self.index):
			self.platform_set.append(self.generate_platform(i, self.score))
	
	#generowanie platform
	def generate_platform(self, index, score):
		"""Generuje platformy"""
		if(score < MAX_JUMP*MAX_JUMP):
			change = int(math.sqrt(score))
		else:
			change = MAX_JUMP-1
		width = 200 - randrange(change, change+60) #długość platformy
		height = 20 #wysokość
		y = 600 - index * 100
		while True:
			side = bool(getrandbits(1))  # losowe 0, 1, współgra z randrange()
			if side:
				x = randrange(self.last_x-MAX_JUMP , self.last_x-change)
			else:
				x = randrange(self.last_x+width+change , self.last_x+MAX_JUMP+width)
			if x >= 0 and x <= SCREEN_WIDTH - width:
				break
		self.last_x = x
		return Platform(x, y, width, height) #tworzenie platformy

	def draw(self, game_display, camera):
		#rywoanie platform na ekranie 
		for p in self.platform_set:
			p.draw(game_display, camera)

	def collide_set(self, player):
		for i,p in enumerate(self.platform_set):
			player.collide_platform(p,i)

	def generate_new_platforms(self, camera):
		#generowanie nowych platform
		if self.platform_set[-1].y - camera.y > -50:
			for i in range(self.index,self.index+10):
				self.platform_set.append(self.generate_platform(i, self.score))
			self.index += 10
