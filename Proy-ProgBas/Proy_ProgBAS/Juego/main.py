import pygame,sys,random

pygame.init()
tamaño=1280,720
ventana = pygame.display.set_mode(tamaño)

clock=pygame.time.Clock()
fondo=pygame.image.load("../assets/Imagenes/espacio.jpg").convert()

#JUGADOR
nave=pygame.image.load("../assets/Imagenes/nave.png").convert()
nave=pygame.transform.scale(nave,(64,64))   
nave.set_colorkey([0,0,0])
x=640
y=360
x_s=0
y_s=0

#DISPARO
laser=pygame.image.load("../assets/Imagenes/laser.png").convert_alpha()
laser=pygame.transform.scale(laser,(10,20))
balas=[]
balas_borrar=[]
laser_speed=10

#METEOROS
meteoros=pygame.image.load("../assets/Imagenes/meteoro.png").convert()
meteoros=pygame.transform.scale(meteoros,(65,65))
def generar_meteoros():
    borde=random.choice(["arriba","abajo","derecha","izquierda"])
    if borde=="arriba":
        x_meteor=random.randint(0,1280)
        y_meteor=-50
        dir_x=random.uniform(-2,2)
        dir_y=random.uniform(1,4)
    elif borde=="abajo":
        x_meteor=random.randint(0,1280)
        y_meteor=720+50
        dir_x=random.uniform(-2,2)
        dir_y=random.uniform(1,4)
    elif borde=="derecha":
        x_meteor=1280+50
        y_meteor=random.randint(0,720)
        dir_x=random.uniform(1,4)
        dir_y=random.uniform(-2,2)
    if borde=="izquierda":
        x_meteor=-50
        y_meteor=random.randint(0,720)
        dir_x=random.uniform(1,4)
        dir_y=random.uniform(-2,2)
        
    return {"x":x_meteor, "y":y_meteor,"dir_x":dir_x,"dir_y":dir_y}
    
            

#SONIDOS
sonido=pygame.mixer.Sound("../assets/sonidos/laser5.ogg")

#AJUSTE DEL TIEMPO
ultimo_spawn=0
meteoritos=[]

#ESTADO DEL JEUGO
muerto=False
pausa=False
puntaje=0
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pausa=not pausa
            if not pausa:
                if event.key==pygame.K_SPACE:
                    balas.append([x+nave.get_width()//2-laser.get_width()//2,y])
                    sonido.play() 
                if event.key==pygame.K_RIGHT:
                    x_s=5
                if event.key==pygame.K_LEFT:
                    x_s=-5
                if event.key==pygame.K_UP:
                    y_s=-5
                if event.key==pygame.K_DOWN:
                    y_s=5
        if event.type==pygame.KEYUP and not pausa:
            if event.key ==pygame.K_LEFT:
                    x_s=0
            if event.key== pygame.K_RIGHT:
                    x_s=0
            if event.key ==pygame.K_UP:
                    y_s=0
            if event.key== pygame.K_DOWN:
                    y_s=0
            
            
             
    ventana.blit(fondo,[0,0])
    
    # MOVIMIENTO Y AJUSTE DE LA NAVE
    x+=x_s
    if x>1216:
        x=1216
    if x<1:
        x=1
    y+=y_s
    if y>656:
        y=656
    if y<1:
        y=1
        
    rect_nave=nave.get_rect(topleft=(x,y))
    for m in meteoritos:
        rect_m=meteoros.get_rect(topleft=(m["x"],m["y"]))
        if rect_nave.colliderect(rect_m):
            muerto=True
            if muerto:
                fuente = pygame.font.SysFont(None, 80)
                texto = fuente.render(f"¡Perdiste!", True, (255, 255, 255))
                ventana.blit(texto, (tamaño[0]//2 - 150, tamaño[1]//2 - 40))

    
    ventana.blit(nave,[x,y])
    
    if not muerto and not pausa:
        #DISPAROS
        for bala in balas:
            bala[1]+=-laser_speed
            
            if bala[1]< -laser.get_height():
                balas_borrar.append(bala)
                continue
            
            rect_bala=laser.get_rect(topleft=(bala[0],bala[1]))
            
            for m in meteoritos:
                rect_m=meteoros.get_rect(topleft=(m["x"],m["y"]))
                if rect_bala.colliderect(rect_m):
                    balas_borrar.append(bala)
                    meteoritos.remove(m)
                    puntaje+=1
                
            if bala not in balas_borrar:
                if bala in balas:
                    ventana.blit(laser,bala)
            
        for bala in balas_borrar:
            if bala in balas:
                balas.remove(bala)
                
        #Creando los meteoritos
        time= pygame.time.get_ticks()
    
        if time - ultimo_spawn>500:
            meteoritos.append(generar_meteoros())
            ultimo_spawn=time
        
        for meteoro in meteoritos:
            meteoro["x"]+= meteoro["dir_x"]
            meteoro["y"]+= meteoro["dir_y"]
            ventana.blit(meteoros,(meteoro["x"],meteoro["y"]))
    if pausa:
        fuente = pygame.font.SysFont(None, 80)
        texto = fuente.render("Pausado", True, (255, 255, 255))
        ventana.blit(texto, (tamaño[0]//2 - 150, tamaño[1]//2 - 40))
        
    pygame.display.flip()
    clock.tick(60)