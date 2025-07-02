import pygame,sys


pygame.init()
tamaño=1280,720
ventana=pygame.display.set_mode(tamaño)

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
blue=(0,0,255)
green=(0,255,0)
dblue=(0,0,204)

#Cargando imagen de fondo

bg=pygame.image.load("../assets/Imagenes/menubg.jpg").convert()
bg=pygame.transform.scale(bg,(1280,720))

clock=pygame.time.Clock()

def menu():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if salir.collidepoint(event.pos):
                    sys.exit()
                elif jugar.collidepoint(event.pos):
                    import main
                    main.juego()
                elif puntajes.collidepoint(event.pos):
                    print("ya va")
            
            
            
        ventana.blit(bg,(0,0))
        
        #BOTON JUGAR
        jugar=pygame.Rect(540,300,200,60)
        pygame.draw.rect(ventana,dblue,jugar)
        fuente= pygame.font.SysFont(None,50)
        texto= fuente.render("JUGAR",True,(white))
        ventana.blit(texto,(jugar.x+45,jugar.y+18))
        
        #BOTON PUNTAJES
        puntajes=pygame.Rect(540,370,200,60)
        pygame.draw.rect(ventana,dblue,puntajes)
        fuente=pygame.font.SysFont(None,50)
        texto=fuente.render("puntajes",True,(white))
        ventana.blit(texto,(puntajes.x+25,puntajes.y+13))
        
        #Boton SALIR
        salir=pygame.Rect(540,440,200,60)
        pygame.draw.rect(ventana,dblue,salir)
        fuente=pygame.font.SysFont(None,50)
        texto=fuente.render("Salir",True,(white))
        ventana.blit(texto,(salir.x+60,salir.y+20))

        
        pygame.display.flip()
        clock.tick(60)
menu()
    