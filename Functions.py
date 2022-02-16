import pygame
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT


def text_objects(text, font, color):
    """Funkcja odpowiedzialna za rysowanie tekstu na powierzchni"""
    textSurface = font.render(text, True, color) #tworzy nową powierzchnię z podanym tekstem
    return textSurface, textSurface.get_rect()#rozmiar

#wyświetlanie tekstu
def message_display(game_display, text, x, y, font_size, color, centered_x=False, centered_y=False):
    """ Służy do wyświetlania tekstu"""
    font = pygame.font.Font(None,font_size) #tworzy czcionkę z podanego pliku
    TextSurf, TextRect = text_objects(text, font, color)
    if centered_x and centered_y:
    	TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
    elif centered_x:
    	TextRect.center = ((SCREEN_WIDTH/2),y)
    elif centered_y:
    	TextRect.center = (x,(SCREEN_HEIGHT/2))
    else:
    	TextRect.center = (x,y)
    
    #rysowanie obrazu na obrazie
    game_display.blit(TextSurf, TextRect)

import os, sys
from pygame.locals import RLEACCEL
def load_image(name, colorkey=None):
    """ 
    Funkcja ładuje obraz i przekształca go w powierzchnię,
    jeśli nie znajdzie obrazu wyrzuca błąd
    """
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)  # plik -> płaszczyzna
    except :
        sys.exit('Cannot load image: %s' % name)
        #raise SystemExit('Cannot load image:', name)
    image = image.convert()  # przekonwertuj na format pikseli ekranu
    colorkey = -1
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL) #ustawia na przezroczysty
    return image


def loadSound(name):
    """
    Funkcja ładuje i włącza dźwiek
    """
    fullname = os.path.join("sounds", name)
    pygame.mixer.init()
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play()
