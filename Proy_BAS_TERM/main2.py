import pygame,sys,random

pygame.init()
tamaño=1280,720
ventana = pygame.display.set_mode(tamaño)
def menu():
    black=(0,0,0)
    white=(255,255,255)
    red=(255,0,0)
    blue=(0,0,255)
    green=(0,255,0)
    dblue=(0,0,204)
    
    #Cargando imagen de fondo

    bg=pygame.image.load("assets/Imagenes/menubg.jpg").convert()
    bg=pygame.transform.scale(bg,(1280,720))

    clock=pygame.time.Clock()


    jugar=pygame.Rect(540,300,200,60)
    opciones=pygame.Rect(540,370,200,60)
    salir=pygame.Rect(540,440,200,60) 
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if salir.collidepoint(event.pos):
                    sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if jugar.collidepoint(event.pos):
                    juego()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if opciones.collidepoint(event.pos):
                    puntajes()
            
            
            
        ventana.blit(bg,(0,0))
        
        #BOTON JUGAR
        
        pygame.draw.rect(ventana,dblue,jugar)
        fuente= pygame.font.SysFont(None,50)
        texto= fuente.render("JUGAR",True,(white))
        ventana.blit(texto,(jugar.x+45,jugar.y+18))
        
        #BOTON OPCIONES
      
        pygame.draw.rect(ventana,dblue,opciones)
        fuente=pygame.font.SysFont(None,40)
        texto=fuente.render("Puntuaciones",True,(white))
        ventana.blit(texto,(opciones.x+10,opciones.y+13))
        
        #Boton SALIR
    
        pygame.draw.rect(ventana,dblue,salir)
        fuente=pygame.font.SysFont(None,50)
        texto=fuente.render("Salir",True,(white))
        ventana.blit(texto,(salir.x+60,salir.y+20))

        
        pygame.display.flip()
        clock.tick(60)
        
def cargar_puntajes(a,b,c):
        try:
            open("puntajes.txt")
        except FileNotFoundError:
            print("creando archivo")
            archivo=open("puntajes.txt","x")
            archivo.close()
        archivo=open("puntajes.txt","a")
        archivo.write(f"Puntaje: {a} || Tiempo:  {b} || Enemigos Eliminados: {c}\n")
        archivo.close()

clock=pygame.time.Clock()



def juego():
    fondo=pygame.image.load("assets/Imagenes/espacio.jpg").convert()
    
    #PUNTUACIONES
    puntaje=0
    tiempo_inicio=pygame.time.get_ticks()
    tiempo=0
    tiempo_jugado=0
    ultimo_tiempo= tiempo_inicio
    enemigos_eliminados=0
    meteoritos_destruidos=0
    
    #FASE DEL JUEGO
    fase_actual="meteoritos"
    duracion_fase =15000 #30 segundos
    tiempo_fase_inicial=pygame.time.get_ticks()
    aliens_generados=False

    #JUGADOR
    nave=pygame.image.load("assets/Imagenes/nave.png").convert()
    nave=pygame.transform.scale(nave,(64,64))   
    nave.set_colorkey([0,0,0])
    x=640
    y=360
    x_s=0
    y_s=0

    #DISPARO
    laser=pygame.image.load("assets/Imagenes/laser.png").convert_alpha()
    laser=pygame.transform.scale(laser,(10,20))
    balas=[]
    balas_borrar=[]
    laser_speed=10

    #METEOROS
    meteoros=pygame.image.load("assets/Imagenes/meteoro.png").convert()
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
    
    #ALIENS
    alien=pygame.image.load("assets/Imagenes/alien_1.png").convert()
    alien=pygame.transform.scale(alien,(50,50))

    alien_speed=5 + (tiempo_jugado//30000)  #+ 1 de velocidad por cada 30 segundos
    
    aliens=[]
    def generar_aliens():
        for fila in range(6):
            for col in range(10):
                x_a= 100+ col* 70
                y_a= 50 +fila *60 
                aliens.append({"x":x_a,"y":y_a,"dir":1})

        
                

    #SONIDOS
    sonido=pygame.mixer.Sound("assets/sonidos/laser5.ogg")

    #AJUSTE DEL TIEMPO
    ultimo_spawn=0
    meteoritos=[]
    
    #Fuentes
    fuente_puntaje=pygame.font.SysFont(None,40)

    #ESTADO DEL JUEGO
    muerto=False
    pausa=False
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if muerto:
                if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                        tiempo=tiempo_jugado//1000
                        puntaje= (meteoritos_destruidos*50)+(enemigos_eliminados*100)
                        cargar_puntajes(puntaje,tiempo,enemigos_eliminados)
                        menu()
                continue
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pausa = not pausa
                    if not pausa:   #Justo cuando se despausa actualizamos al tiempo anterior
                        ultimo_tiempo=pygame.time.get_ticks() #Se evita un salto
                tiempo_actual=pygame.time.get_ticks()        
                if not pausa and not muerto:
                    tiempo_actual=pygame.time.get_ticks()
                    tiempo_jugado += tiempo_actual-ultimo_tiempo  
                    ultimo_tiempo=tiempo_actual
                    
                elif pausa or muerto:
                    x_s=0
                    y_s=0
                    pass
                
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
        
        if muerto:
            x_s=0
            y_s=0
            
        rect_nave=nave.get_rect(topleft=(x,y))
        
        #METEOROS
        for m in meteoritos:
            rect_m=meteoros.get_rect(topleft=(m["x"],m["y"]))
            if rect_nave.colliderect(rect_m):
                muerto=True
        if fase_actual=="aliens":
            for alien_info in aliens:
                rect_alien=alien.get_rect(topleft=(alien_info["x"],alien_info["y"]))
                if rect_nave.colliderect(rect_alien):
                    muerto= True
        if muerto:
            fuente = pygame.font.SysFont(None, 80)
            texto = fuente.render("¡Perdiste!", True, (255, 255, 255))
            ventana.blit(texto, (tamaño[0]//2 - 150, tamaño[1]//2 - 40))
                    
            fuente2 = pygame.font.SysFont(None,60)
            texto2 = fuente2.render("Presiona ENTER para volver al menu",True,(255,255,255))
            ventana.blit(texto2,(250,380))
                    

        #CAMBIO DE FASE
        tiempo_actual=pygame.time.get_ticks()
        if tiempo_actual - tiempo_fase_inicial>duracion_fase:
            if fase_actual=="meteoritos":
                if tiempo_actual - tiempo_fase_inicial>duracion_fase:
                    fase_actual="aliens"
                    aliens_generados=False
                    tiempo_fase_inicial=tiempo_actual
            elif fase_actual=="aliens":
                if len(aliens)==0:
                    fase_actual="meteoritos"
                    tiempo_fase_inicial=tiempo_actual
                
            tiempo_fase_inicial=tiempo_actual
            balas.clear()
       
        
        if not muerto and not pausa:
            
            ventana.blit(nave,[x,y])  

        
        # GENERAR ALIENS si toca
            if fase_actual == "aliens" and not aliens_generados:
                generar_aliens()
                aliens_generados = True

        # MOVER Y DIBUJAR ALIENS (solo si estamos en fase de aliens)
            if fase_actual == "aliens":
                for alien_info in aliens:
                    alien_info["x"] += alien_info["dir"] * alien_speed
                    # Cambiar de dirección si tocan el borde
                    if alien_info["x"] < 0 or alien_info["x"] > 1280 - 50:
                        alien_info["dir"] *= -1
                        alien_info["y"] += 40  # bajan un poco
                    if alien_info["y"]+ alien.get_height()>=720:
                        muerto=True
                    ventana.blit(alien, (alien_info["x"], alien_info["y"]))

            # DISPAROS
            for bala in balas[:]:  # Usamos copia para evitar errores al modificar la lista
                bala[1] -= laser_speed

                if bala[1] < -laser.get_height():
                    balas.remove(bala)
                    continue

                rect_bala = laser.get_rect(topleft=(bala[0], bala[1]))

                # Colisión con meteoritos
                for m in meteoritos:
                    rect_m = meteoros.get_rect(topleft=(m["x"], m["y"]))
                    if rect_bala.colliderect(rect_m):
                        if bala in balas:
                            balas.remove(bala)
                        if m in meteoritos:
                            meteoritos.remove(m)
                            meteoritos_destruidos += 1
                        break

                # Colisión con aliens
                if fase_actual == "aliens":
                    for alien_info in aliens:
                        rect_alien = alien.get_rect(topleft=(alien_info["x"], alien_info["y"]))
                        if rect_bala.colliderect(rect_alien):
                            if bala in balas:
                                balas.remove(bala)
                            if alien_info in aliens:
                                aliens.remove(alien_info)
                                enemigos_eliminados += 1
                            break

                if bala in balas:  # Solo dibujamos si no fue eliminada
                    ventana.blit(laser, bala)

                    
            #Creando los meteoritos
            time= pygame.time.get_ticks()
            if fase_actual=="meteoritos":
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
           
        
        #DIBUJO DE LOS TEXTOS PUNTAJE-TIEMPO
        puntaje=(meteoritos_destruidos*50)+(enemigos_eliminados*100)
        tiempo=tiempo_jugado//1000  # ticks = tiempo en milisegundos -> segundos = ticks/1000 
        texto_puntaje=fuente_puntaje.render(f"Puntaje: {puntaje}         Tiempo: {tiempo}",True,(255,255,255))
        ventana.blit(texto_puntaje,(20,20))
        
         
        pygame.display.flip()
        clock.tick(60)  #aprox 16 milisegundos ; 1 seg = 60 ticks

def ordenar_puntajes():
    try:
        archivo=open("puntajes.txt","rt")
        puntajes = []
        for linea in archivo:
            linea = linea.strip().split()
            if linea:  
                puntajes.append((linea))  
        puntajes=sorted(puntajes, key=lambda x: int(x[1]), reverse=True)  
            
        archivo.close()
        archivo = open("puntajes.txt", "w")
        for i in range(len(puntajes)):
            for j in range(len(puntajes[i])):
                puntaje=puntajes[i][j]
                archivo.write(puntaje + " ")
                if j == 8:
                    archivo.write("\n")
        archivo.close()
    except FileNotFoundError:
        pass

#ventana puntajes
def puntajes():
    black=(0,0,0)
    white=(255,255,255)
    red=(255,0,0)
    blue=(0,0,255)
    green=(0,255,0)
    dblue=(0,0,204)
    
    #Cargando imagen de fondo

    bg=pygame.image.load("assets/Imagenes/menubg.jpg").convert()
    bg=pygame.transform.scale(bg,(1280,720))

    clock=pygame.time.Clock()



    volver=pygame.Rect(540,650,200,60) 
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if volver.collidepoint(event.pos):
                    menu()
        
        ventana.blit(bg,(0,0))
        
        #Boton volver
    
        pygame.draw.rect(ventana,dblue,volver)
        fuente=pygame.font.SysFont(None,50)
        texto=fuente.render("Volver",True,(white))
        ventana.blit(texto,(volver.x+50,volver.y+15))

        
        pygame.display.flip()
        clock.tick(60)


#EJECUCION        
menu()