from Functions import *
import pygame

# Inicjalizacja PyGame
pygame.init()

from copy import deepcopy

class Platform:
	"""Klasa opisująca platformy"""
	color = (255, 100, 100)
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.rect = pygame.Rect(x, y, width, height)#współrzędne
		self.collected_score = False

	def draw(self, game_display, camera):
		rect = deepcopy(self.rect)
		rect.top -= camera.y
		#rysuj prostokąt
		pygame.draw.rect(game_display, self.color, rect)
		for i in range(self.x, self.x + self.width, 10):
			sprite = IceSprite([i, self.y - camera.y])
			#załaduj plik
			game_display.blit(sprite.image, sprite.rect)	


class IceSprite(pygame.sprite.Sprite):
	"""Inicjalizuj klasę bazową lodu(platform)"""
	image = None

	def __init__(self, location):
		#Inicjalizuje wygląd lodu
		pygame.sprite.Sprite.__init__(self)

		if IceSprite.image is None:
			IceSprite.image = load_image("ice.png")

		self.image = IceSprite.image

		self.rect = self.image.get_rect()  # rozmiar rysunku
		self.rect.topleft = location  # gdzie wstawić
