from Functions import load_image
import pygame

# Inicjalizacja PyGame
pygame.init()

from Constants import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT

from copy import deepcopy

class Player:
	"""Klasa opisująca wygląd i zachowanie gracza"""

	width = 30
	height = 50

	#początkowe
	vel_x = 0
	vel_y = 0

	max_falling_speed = 20

	#przyśpieszenie
	acceleration = 0.5
	max_vel_x = 7

	color = (255, 0, 0)
	speed = 5

	def __init__(self):
		self.x = 30
		self.y = 500
		self.score = -10 # odjąc podstawową platforme

		self.spritesheet_image = load_image('spritesheet.png')
		self.spritesheet = [] #lista na wygląd gracza

		# Gdy stoi w miejscu
		# SRCALPHA – oznacza, że format pikseli będzie zawierać ustawienie alfa (przezroczystości)
		self.cropped = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped.blit(self.spritesheet_image, (0, 0), (0, 0, 33, 57))
		self.cropped2 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped2.blit(self.spritesheet_image, (0, 0), (37, 0, 33, 57))
		self.cropped3 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped3.blit(self.spritesheet_image, (0, 0), (75, 0, 33, 57))
		self.spritesheet.append(self.cropped)
		self.spritesheet.append(self.cropped2)
		self.spritesheet.append(self.cropped3)
		
		# Gdy idziemy w prawo
		self.cropped4 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped4.blit(self.spritesheet_image, (0, 0), (0, 56, 33, 57))
		self.cropped5 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped5.blit(self.spritesheet_image, (0, 0), (37, 56, 33, 57))
		self.cropped6 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped6.blit(self.spritesheet_image, (0, 0), (75, 56, 33, 57))
		self.spritesheet.append(self.cropped4)
		self.spritesheet.append(self.cropped5)
		self.spritesheet.append(self.cropped6)

		#odwróć - gdy idziemy w lewo
		self.spritesheet.append(pygame.transform.flip(self.cropped4, True, False))
		self.spritesheet.append(pygame.transform.flip(self.cropped5, True, False))
		self.spritesheet.append(pygame.transform.flip(self.cropped6, True, False))

		# Gdy skaczemy
		self.cropped7 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped7.blit(self.spritesheet_image, (0, 0), (75, 112, 33, 57))
		self.spritesheet.append(self.cropped7)
		self.spritesheet.append(self.cropped7)
		self.spritesheet.append(self.cropped7)

		self.sprite_index_x = 0
		self.sprite_index_y = 0
		self.frame_counter = 0
		self.frame_delay = 9 #opóźnienie

	def draw(self, game_display, camera):
		"""Funkcja rysuje gracza na ekranie"""
		#ładowanie obrazu gracza
		game_display.blit(self.spritesheet[self.sprite_index_y*3 + self.sprite_index_x], (self.x, self.y-camera.y))

		self.frame_counter += 1
		if self.frame_counter >= self.frame_delay:
			self.sprite_index_x += 1
			if self.sprite_index_x > 2:
				self.sprite_index_x = 0
			self.frame_counter = 0
	
	def update(self):
		#aktualizacja
		self.x += self.vel_x
		self.y += self.vel_y
		self.vel_y += GRAVITY
		if self.vel_y > self.max_falling_speed:
			self.vel_y = self.max_falling_speed
		if self.x <= 0:
			self.x = 0
		if self.x + self.width >= SCREEN_WIDTH:
			self.x = SCREEN_WIDTH - self.width

	def combo(self):
		"""Funkcja odpowiedzialna za combo"""
		#combo - "wzmacnianie" skoku
		if self.x == 0:
			if self.vel_y < 0:
				if self.vel_x < 0:
					self.vel_y -= 10
					self.vel_x *= -2.5
		if self.x + self.width >= SCREEN_WIDTH:
			if self.vel_y < 0:
				if self.vel_x > 0:
					self.vel_y -= 10
					self.vel_x *= -2.5

	def on_platform(self, platform):
		#sprawdź, czy punkt znajduje się w prostokącie, zwraca boola(sprawdzanie czy postać jest na platformie)
		return platform.rect.collidepoint((self.x, self.y + self.height)) or \
			platform.rect.collidepoint((self.x+self.width, self.y + self.height))

	def on_any_platform(self, platform_controller, floor):
		for p in platform_controller.platform_set:
			if self.on_platform(p):
				return True
		if self.on_platform(floor):
			#czy gracz jest na platformie
			return True
		return False
	
	#sprawdzanie, czy nachodzą na siebie
	def collide_platform(self, platform, index):
		for i in range(0,self.vel_y):
			#czy dwa prostokąty nachodzą na siebie
			if pygame.Rect(self.x, self.y-i, self.width, self.height).colliderect(platform.rect):
				if platform.rect.collidepoint((self.x, self.y + self.height-i)) or \
		 	platform.rect.collidepoint((self.x+self.width, self.y + self.height-i)): 
					self.y = platform.y - self.height
					if not platform.collected_score:
						self.score += 10
						if self.score < index * 10:
							self.score = index * 10
						platform.collected_score = True

	
	#przechowuje współrzędne
	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

	#spadnięcie poza ekran
	def fallen_off_screen(self, camera):
		if self.y - camera.y + self.height >= SCREEN_HEIGHT:
			return True
		return False
