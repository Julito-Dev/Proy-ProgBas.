import os
import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"Imagenes/alien_{type}.png" 
        
        try:
            self.image = pygame.image.load(path)
        except FileNotFoundError:
            print(f"ERROR: No se encontró la imagen del alien '{path}'.")
            print("Asegúrate de que las imágenes de alien están en la carpeta correcta y los nombres son exactos (alien_1.png, etc.).")
            self.image = pygame.Surface((35, 30)) 
            self.image.fill((255, 0, 255)) 

        scale_width = 35  
        scale_height = 30
        self.image = pygame.transform.scale(self.image, (scale_width, scale_height))
        
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, direction):
        self.rect.x += direction

class Game: 
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height 
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens() 
        
        self.aliens_direction = 1  
        self.alien_speed = 1       
        self.alien_drop_speed = 20 
    
    def create_aliens(self): 
        for row in range(5):    
            for column in range(11): 
                x = 10 + column * 55 
                y = 10 + row * 55    

                if row == 0: 
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else: 
                    alien_type = 1

                alien = Alien(alien_type, x, y)
                self.aliens_group.add(alien)

    def move_aliens(self): 
        self.aliens_group.update(self.aliens_direction * self.alien_speed)

        hit_edge = False
        for alien in self.aliens_group.sprites():
            if alien.rect.right >= self.screen_width or alien.rect.left <= 0:
                hit_edge = True 
            
            if alien.rect.top >= self.screen_height:
                alien.kill() 

        if hit_edge:
            self.aliens_direction *= -1 
            self.drop_aliens()          

        if not self.aliens_group: 
            print("Todos los aliens eliminados. Generando una nueva oleada.") 
            self.create_aliens() 

    def drop_aliens(self):
        for alien in self.aliens_group.sprites():
            alien.rect.y += self.alien_drop_speed