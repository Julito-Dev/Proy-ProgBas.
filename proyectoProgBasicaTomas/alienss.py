import os
import pygame, sys
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Space Invaders")

clock = pygame.time.Clock()
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

try:
    background_image = pygame.image.load("Imagenes/espacio.jpg").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("No se encontró la imagen de fondo 'Imagenes/espacio.jpg'.")
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_image, (0, 0))

    game.move_aliens()

    game.aliens_group.draw(screen)

    pygame.display.update()

    clock.tick(60)