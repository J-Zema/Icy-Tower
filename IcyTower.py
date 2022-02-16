from Functions import *
import pygame
from Camera import Camera
from Player import Player 
from Platform import Platform
from PlatformController import PlatformController

# Inicjalizacja PyGame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

#majlepsze wyniki
BEST = []

from Constants import *

# Tworzenie okna
game_display = pygame.display.set_mode(res)
pygame.display.set_caption(GAME_CAPTION)

black = (0,0,0) 
blue = (0,0, 255)
white = (255,255,255)

#wznowienie gry
def reinit():
	"""Funkcja wznawia grę"""
	global player
	global platform_controller
	global floor
	global camera
	player = Player()
	platform_controller = PlatformController()
	floor = Platform(0, SCREEN_HEIGHT-36, SCREEN_WIDTH, 36)
	camera = Camera(player)


#inicjalizuje gracza
player = Player()
platform_controller = PlatformController()

#podstawowa platforma
floor = Platform(0, SCREEN_HEIGHT-36, SCREEN_WIDTH, 36)

#strzałka
arrow_image = load_image("arrow.png")

#do wyboru w menu
selected_option = 0.30

#tło
background = load_image('background.jpg')

camera = Camera(player)

#stan gry
game_state = 'Menu'
game_loop = True

# do śledzenia czasu
clock = pygame.time.Clock()
fps = 60

while game_loop:
	
	#ruchy
	for event in pygame.event.get(): #pobiera zdarzenia
		if event.type == pygame.QUIT:
			game_loop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if game_state == 'Playing' or game_state == 'Game Over' or game_state == 'About' or game_state == 'Rules' or game_state == 'Best':
					game_state = 'Menu'
			elif game_state == 'Game Over':#po naciśnieciu spacji wraca do gry
				if event.key == pygame.K_SPACE:
					reinit()
					game_state = 'Playing'
			elif game_state == "Menu": #Poruszanie się po menu
				if event.key == pygame.K_DOWN:
					if selected_option<0.65:
						selected_option+=0.10 
					else:
						selected_option=0.30
				elif event.key == pygame.K_UP:
					if selected_option>0.35:
						selected_option-=0.10
					else: 
						selected_option=0.70
				elif event.key == pygame.K_RETURN:
					if selected_option < 0.35:
						reinit()
						game_state = 'Playing'
					elif selected_option == 0.40:
						game_state = 'Rules'
					elif selected_option == 0.50:
						game_state = 'Best'
					elif selected_option == 0.60:
						game_state = 'About'
					elif selected_option == 0.70:
						game_loop = False

	#stan wszystkich przycisków, informuje, czy dany klawisz jest trzymany wciśnięty
	keys_pressed = pygame.key.get_pressed()

	#ruchy gracza
	if keys_pressed[pygame.K_LEFT]:
		player.vel_x -= player.acceleration
		if player.vel_x < -player.max_vel_x:
			player.vel_x = -player.max_vel_x
		player.sprite_index_y = 2
	elif keys_pressed[pygame.K_RIGHT]:
		player.vel_x += player.acceleration
		if player.vel_x > player.max_vel_x:
			player.vel_x = player.max_vel_x
		player.sprite_index_y = 1
	else:
		if player.vel_x < 0:
			player.vel_x += player.acceleration
			player.vel_x -= ICE_RESISTANCE
			if player.vel_x > 0:
				player.vel_x = 0
		else:
			player.vel_x -= player.acceleration
			player.vel_x += ICE_RESISTANCE
			if player.vel_x < 0:
				player.vel_x = 0

		if player.vel_y >= JUMP_VELOCITY/2:
			player.sprite_index_y = 0

	#------------------------------------------------------------------------
	# MENU
	#-----------------------------------------------------------------------

	if game_state == "Menu":
		#załaduj plik
		game_display.blit(background,(0,0))

		#strzałka
		game_display.blit(arrow_image, (MENU_START_X + ARROW_HALF_WIDTH, MENU_START_Y + SCREEN_HEIGHT*selected_option - ARROW_HALF_HEIGHT))
		if pygame.font:
			
			#nazwa gry
			message_display(game_display, "Icy Tower", 0, MENU_START_Y + round(SCREEN_HEIGHT*0.15), 60, white, True)
			
			#składniki menu
			message_display(game_display, "Play", 0, MENU_START_Y + round(SCREEN_HEIGHT*0.30), 50, white, True)
			message_display(game_display, "Rules", 0, MENU_START_Y + round(SCREEN_HEIGHT*0.40), 50, white, True)
			message_display(game_display, "Best", 0, MENU_START_Y + round(SCREEN_HEIGHT*0.50), 50, white, True)
			message_display(game_display, "About", 0, MENU_START_Y + round(SCREEN_HEIGHT*0.60), 50, white, True)
			message_display(game_display, "Quit", 0, MENU_START_Y + round(SCREEN_HEIGHT*0.70), 50, white, True)
	
	#------------------------------------------------------------------------
	# PLAYING
	#-----------------------------------------------------------------------
	elif game_state == 'Playing':

		if keys_pressed[pygame.K_SPACE]: #po naciśnieciu spacji
			if player.on_any_platform(platform_controller, floor):
				loadSound("jump.mp3") #dźwiek
				player.sprite_index_y = 3
				if player.vel_y >= JUMP_VELOCITY/2:
					player.vel_y = -JUMP_VELOCITY
		

		#aktualizacja
		player.update()
		player.combo()
		player.collide_platform(floor,0)
		platform_controller.collide_set(player)

		#punkty i aktualizacja
		platform_controller.score = player.score
		camera.update(player.score)

		#generowanie platform
		platform_controller.generate_new_platforms(camera)

		if player.fallen_off_screen(camera):#gry spadnie poza ekran
			#zapis punktów
			with open('score.txt', 'a') as file:
				file.write(str(player.score)+"\n")
			game_state = 'Game Over'

		#załaduj plik
		game_display.blit(background,(0,0))

		#rysowanie obiektów
		floor.draw(game_display, camera)
		platform_controller.draw(game_display, camera)
		player.draw(game_display, camera)
		
		#wyświetlanie punktów
		message_display(game_display, str(player.score), 25, 30, 36, white)

	#------------------------------------------------------------------------
	# GAME OVER
	#-----------------------------------------------------------------------
	elif game_state == 'Game Over':
		#załaduj plik
		game_display.blit(background,(0,0))
		if pygame.font:
		    message_display(game_display, "GAME OVER", 0, 200, 70, white, True)
		    message_display(game_display, "Score: %d" % player.score, 0, 300, 50, white, True)
		    message_display(game_display, "Press SPACE to play again!", 0, 400, 50, white, True)
		    message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, white, True)
		

	#------------------------------------------------------------------------
	# ABOUT
	#-----------------------------------------------------------------------
	elif game_state == 'About':
		#załaduj plik
		game_display.blit(background,(0,0))	
		if pygame.font:
			for line in ABOUT_MESSAGE:
				message_display(game_display, line, 0, MENU_START_Y + ABOUT_MESSAGE.index(line)*35, 30, white, True)
			message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, white, True)
				
	#------------------------------------------------------------------------
	# RULES
	#-----------------------------------------------------------------------
	elif game_state == 'Rules':
		#załaduj plik
		game_display.blit(background, (0, 0))
		if pygame.font:
			for line in RULES_MESSAGE:
				message_display(game_display, line, 0, MENU_START_Y +
				                RULES_MESSAGE.index(line)*35, 30, white, True)
			message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, white, True)

	#------------------------------------------------------------------------
	# BEST
	#-----------------------------------------------------------------------
	elif game_state == 'Best':
		NUMBERS = [] #Str -> Int
		BEST_RANKING = ["Best scores:"] #Int -> Str
		with open('score.txt', 'r') as file:
			BEST = file.readlines()
			for i in range(len(BEST)):
				a = BEST[i]
				if int(a) in NUMBERS:
					continue
				else:
					NUMBERS.sort(reverse=True)
					if len(NUMBERS) > 10:
						NUMBERS.pop() #usuwanie ostatniego najgorszego wyniku
					else:
						NUMBERS.append(int(a))
			NUMBERS.sort(reverse=True)#sortowanie 
			for i in range(len(NUMBERS)):
				b = NUMBERS[i]
				BEST_RANKING.append(str(b))

		#załaduj plik
		game_display.blit(background, (0, 0))

		if pygame.font:
			for line in BEST_RANKING:
				message_display(game_display, line, 0, MENU_START_Y +
				                BEST_RANKING.index(line)*35, 30, white, True)
			message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, white, True)

	pygame.display.update()
	clock.tick(fps)
	

pygame.quit()	
#quit()
