import pygame
import random
import pyttsx3
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import obter_nivel

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()
voz = pyttsx3.init()
# Marcão esteve aqui
while True:
    nome = input("NickName:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Dragon Escape")
icone  = pygame.image.load("base/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("base/backgroundV2.png")
fundoDead = pygame.image.load("base/backgroundDead.png")
fundoStart = pygame.image.load("base/backgroundStart.png")

dragon = pygame.image.load("base/Dragon.png")
dragon = pygame.transform.scale(dragon, (280,180))
missel = pygame.image.load("base/lança.png")
missel = pygame.transform.scale(missel, (180,180))
missileSound = pygame.mixer.Sound("base/missile.wav")
explosaoSound = pygame.mixer.Sound("base/explosao.wav")
pygame.mixer.music.load("base/ironsound.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fontePause = pygame.font.SysFont("Arial", 60, True)
fonteAjuda = pygame.font.SysFont("Arial", 18)
nuvem = pygame.image.load("base/nuvem.png")
nuvem = pygame.transform.scale(nuvem, (120, 80))

def jogar():
    fundoMov1 = 0
    fundoMov2 = 1000
    velocidadeFundo = 1
    posicaoXPersona = 180
    posicaoYPersona = 60
    movimentoYPersona  = 0
    velocidadeMovPersona = 5
    posicaoXMissel = 800
    posicaoYMissel = 100
    velocidadeMissel = 2
    posicaoXNuvem = 1000
    posicaoYNuvem = random.randint(0, 200)
    velocidadeNuvem = 2
    pontos = 0
    nivel_atual = "Iniciante"
    pausado = False
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
        
        if not pausado:
            posicaoYPersona = posicaoYPersona + movimentoYPersona            
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona > 685:
            posicaoXPersona = 685
        if posicaoYPersona < 0 :
            posicaoYPersona = 0
        elif posicaoYPersona > 450:
            posicaoYPersona = 450
            
            
        if not pausado:
            posicaoXMissel = posicaoXMissel - velocidadeMissel
        if posicaoXMissel < -125:
            pygame.mixer.Sound.play(missileSound)
            posicaoXMissel = 800
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1

            novo_nivel = obter_nivel(pontos)

            if novo_nivel != nivel_atual:
                nivel_atual = novo_nivel
                voz.say("Nivel " + novo_nivel)
                voz.runAndWait()

            velocidadeFundo = velocidadeFundo + 0.3
            posicaoYMissel = random.randint(0,1000)

        if not pausado:
            posicaoXNuvem -= velocidadeNuvem

        if posicaoXNuvem < -120:
            posicaoXNuvem = 1000
            posicaoYNuvem = random.randint(0, 200)                    
        tela.fill(branco)
        tela.blit(fundo, (fundoMov1,0) )
        tela.blit(fundo, (fundoMov2,0) )
        if not pausado:
            fundoMov1 -= velocidadeFundo
            fundoMov2 -= velocidadeFundo
        if fundoMov1 < -1000:
            fundoMov1 = 1000
        elif fundoMov2 < -1000:
            fundoMov2 = 1000
        
        tela.blit(fundo, (fundoMov1,0))
        tela.blit(fundo, (fundoMov2,0))

        tela.blit(nuvem, (posicaoXNuvem, posicaoYNuvem))
        velocidadeNuvem = random.randint(1, 5)
        tela.blit(dragon, (posicaoXPersona,posicaoYPersona))
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))
        
        nivel = obter_nivel(pontos)
        textoNivel = fonteMenu.render("Nivel: " + nivel, True, branco)
        tela.blit(textoNivel, (700, 40))

        textoAjuda = fonteAjuda.render("Press Space to Pause Game", True, branco)
        tela.blit(textoAjuda, (10, 10))

        if pausado:
            textoPause = fontePause.render("PAUSE", True, branco)
            rectPause = textoPause.get_rect(center=(500, 350))
            tela.blit(textoPause, rectPause)
        
            
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+51))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + 125))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + 25))
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (480,15))
        

        pygame.display.update()
        relogio.tick(60)
           
start()