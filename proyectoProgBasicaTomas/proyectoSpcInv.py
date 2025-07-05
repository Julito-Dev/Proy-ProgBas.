import pygame
import os
import random

# --- 1. Inicialización de Pygame ---
pygame.init()

# --- 2. Configuración de la Ventana del Juego ---
ANCHO, ALTO = 800, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")

# --- 3. Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# --- 4. Cargar Imágenes ---
# Asegúrate de tener estas imágenes en la misma carpeta que tu script.
# Si no las tienes, el código usará un simple rectángulo.
DIRECTORIO_ACTUAL = os.path.dirname(__file__)

IMAGEN_NAVE = None
IMAGEN_BALA = None
IMAGEN_ALIEN = None

try:
    IMAGEN_NAVE = pygame.image.load(os.path.join(DIRECTORIO_ACTUAL, "nave.png")).convert_alpha()
    IMAGEN_BALA = pygame.image.load(os.path.join(DIRECTORIO_ACTUAL, "bala.png")).convert_alpha()
    IMAGEN_ALIEN = pygame.image.load(os.path.join(DIRECTORIO_ACTUAL, "alien.png")).convert_alpha()

    IMAGEN_NAVE = pygame.transform.scale(IMAGEN_NAVE, (50, 50))
    IMAGEN_BALA = pygame.transform.scale(IMAGEN_BALA, (10, 30))
    IMAGEN_ALIEN = pygame.transform.scale(IMAGEN_ALIEN, (40, 40))
except pygame.error as e:
    print(f"Advertencia: No se encontraron una o más imágenes. Se usarán formas básicas. Error: {e}")
    IMAGEN_NAVE = None
    IMAGEN_BALA = None
    IMAGEN_ALIEN = None

# --- 5. Clases de los Elementos del Juego ---

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if IMAGEN_NAVE:
            self.image = IMAGEN_NAVE
        else:
            self.image = pygame.Surface([50, 50])
            self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.velocidad = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_balas.add(bala)
        todos_los_sprites.add(bala)


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if IMAGEN_BALA:
            self.image = IMAGEN_BALA
        else:
            self.image = pygame.Surface([5, 15])
            self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = -10 # Negativo para que suba

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if IMAGEN_ALIEN:
            self.image = IMAGEN_ALIEN
        else:
            self.image = pygame.Surface([40, 40])
            self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # La velocidad del alien individual se actualizará por la lógica de la flota.
        # Aquí no necesitamos una velocidad_x individual.

    def update(self):
        # La actualización del movimiento de los aliens se maneja a nivel de la flota.
        pass # No hace nada aquí, su posición se cambia directamente en el bucle principal.


# --- 6. Grupos de Sprites ---
todos_los_sprites = pygame.sprite.Group()
todas_las_balas = pygame.sprite.Group()
todos_los_aliens = pygame.sprite.Group()

# --- 7. Crear el Jugador ---
jugador = Jugador()
todos_los_sprites.add(jugador)

# --- 8. Crear la Flota de Aliens ---
# Variables para la cuadrícula de aliens
NUM_FILAS_ALIENS = 5
NUM_ALIENS_POR_FILA = 10
MARGEN_SUPERIOR = 50
ESPACIADO_X = 60 # Espacio horizontal entre aliens
ESPACIADO_Y = 50 # Espacio vertical entre filas de aliens

for fila in range(NUM_FILAS_ALIENS):
    for columna in range(NUM_ALIENS_POR_FILA):
        # Calcula la posición X para centrar la flota
        x_inicial_flota = (ANCHO - (NUM_ALIENS_POR_FILA * ESPACIADO_X)) // 2
        x = x_inicial_flota + columna * ESPACIADO_X
        y = fila * ESPACIADO_Y + MARGEN_SUPERIOR
        alien = Alien(x, y)
        todos_los_aliens.add(alien)
        todos_los_sprites.add(alien)

# Variables para el movimiento de la flota alienígena
velocidad_flota_horizontal = 1.5 # Velocidad horizontal de toda la flota
velocidad_flota_descenso = 25   # Cuánto baja la flota cuando golpea el borde
direccion_flota = 1             # 1 para derecha, -1 para izquierda

# --- 9. Bucle Principal del Juego ---
juego_en_ejecucion = True
reloj = pygame.time.Clock()
FPS = 60

while juego_en_ejecucion:
    # --- 9.1. Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_en_ejecucion = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jugador.disparar()

    # --- 9.2. Actualizar ---
    # Actualizar todos los sprites (jugador y balas)
    todos_los_sprites.update()

    # --- Lógica de Movimiento de la Flota Alienígena ---
    cambio_de_direccion_necesario = False
    for alien in todos_los_aliens:
        # Mover cada alien horizontalmente según la dirección actual de la flota
        alien.rect.x += velocidad_flota_horizontal * direccion_flota

        # Verificar si algún alien ha llegado a los bordes de la pantalla
        if alien.rect.right >= ANCHO or alien.rect.left <= 0:
            cambio_de_direccion_necesario = True # Activamos la bandera
    
    if cambio_de_direccion_necesario:
        direccion_flota *= -1 # Invertimos la dirección de la flota
        for alien in todos_los_aliens:
            alien.rect.y += velocidad_flota_descenso # Bajamos toda la flota

    # --- Detección de Colisiones (Bala vs Alien) ---
    # Colisiones: balas que golpean aliens. True, True significa que ambos sprites se eliminan.
    colisiones = pygame.sprite.groupcollide(todas_las_balas, todos_los_aliens, True, True)
    
    # Aquí puedes añadir lógica de puntuación, sonidos, etc.
    if colisiones: # Si hubo alguna colisión
        print(f"¡Alien golpeado! Quedan {len(todos_los_aliens)} aliens.")
        # Ejemplo de sonido al destruir alien (necesitarías un archivo 'explosion.wav')
        # try:
        #     sonido_explosion = pygame.mixer.Sound(os.path.join(DIRECTORIO_ACTUAL, "explosion.wav"))
        #     sonido_explosion.play()
        # except pygame.error:
        #     print("Advertencia: No se encontró el archivo de sonido 'explosion.wav'.")

    # --- 9.3. Dibujar/Renderizar ---
    PANTALLA.fill(NEGRO) # Limpiar la pantalla con un fondo negro
    todos_los_sprites.draw(PANTALLA) # Dibujar todos los sprites en la pantalla

    # --- 9.4. Actualizar la Pantalla ---
    pygame.display.flip()

    # --- 9.5. Control de FPS ---
    reloj.tick(FPS)

# --- 10. Salir de Pygame ---
pygame.quit()