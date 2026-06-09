import pygame
import random
import math
import pyttsx3
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import obter_nivel
#Marcão esteve aqui
limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()
voz = pyttsx3.init()

while True:
    nome = input("NickName:")
    if len(nome) > 0:
        break
    else:
        print("Nome Inválido!")

tamanho = (1000, 700)
pygame.display.set_caption("Dragon Escape")
icone = pygame.image.load("base/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("base/backgroundV2.png")
fundoDead = pygame.image.load("base/backgroundDead.png")
fundoStart = pygame.image.load("base/backgroundStart.png")

dragon = pygame.image.load("base/Dragon.png")
dragon = pygame.transform.scale(dragon, (280, 180))
lanca = pygame.image.load("base/lança.png")
lanca = pygame.transform.scale(lanca, (180, 180))

DRAGON_W, DRAGON_H = 280, 180
lanca_W, lanca_H = 180, 180

DRAGON_HB_W, DRAGON_HB_H = 140, 70
DRAGON_HB_OX, DRAGON_HB_OY = 40, 55
lanca_HB_W, lanca_HB_H = 80, 30
lanca_HB_OX, lanca_HB_OY = 20, 75

lancaSound = pygame.mixer.Sound("base/missile.wav")
explosaoSound = pygame.mixer.Sound("base/explosao.wav")
pygame.mixer.music.load("base/ironsound.mp3")

fonteMenu = pygame.font.SysFont("comicsans", 18)
fontePause = pygame.font.SysFont("Arial", 60, True)
fonteAjuda = pygame.font.SysFont("Arial", 18)
fonteBoasVindas = pygame.font.SysFont("comicsans", 32, True)
fonteTitulo = pygame.font.SysFont("comicsans", 22, True)
fonteTexto = pygame.font.SysFont("comicsans", 17)

nuvem = pygame.image.load("base/nuvem.png")
nuvem = pygame.transform.scale(nuvem, (120, 80))

SOL_COR_NUCLEO = (255, 240, 80)
SOL_COR_MEIO   = (255, 200, 0)
SOL_COR_BRILHO = (255, 160, 0)
SOL_RAIO_BASE  = 38
SOL_AMPLITUDE  = 4
SOL_VELOCIDADE = 0.018


def desenhar_sol(tela, fase):
    x = tamanho[0] - 70
    y = 70
    raio = int(SOL_RAIO_BASE + SOL_AMPLITUDE * math.sin(fase))

    aureola = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)
    pygame.draw.circle(aureola, (255, 200, 0, 40), (raio * 2, raio * 2), raio * 2)
    pygame.draw.circle(aureola, (255, 210, 0, 70), (raio * 2, raio * 2), int(raio * 1.55))
    tela.blit(aureola, (x - raio * 2, y - raio * 2))

    pygame.draw.circle(tela, SOL_COR_BRILHO, (x, y), int(raio * 1.25))
    pygame.draw.circle(tela, SOL_COR_MEIO, (x, y), raio)
    pygame.draw.circle(tela, SOL_COR_NUCLEO, (x, y), int(raio * 0.6))


def jogar():
    fundoMov1 = 0
    fundoMov2 = 1000
    velocidadeFundo = 1
    posicaoXPersona = 180
    posicaoYPersona = 60
    movimentoYPersona = 0
    velocidadeMovPersona = 5
    posicaoXlanca = 800
    posicaoYlanca = 100
    velocidadelanca = 2
    posicaoXNuvem = 1000
    posicaoYNuvem = random.randint(0, 200)
    velocidadeNuvem = 2
    pontos = 0
    nivel_atual = "Iniciante"
    pausado = False
    fase_sol = 0.0
    pygame.mixer.Sound.play(lancaSound)
    pygame.mixer.music.play(-1)

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
        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > 685:
            posicaoXPersona = 685
        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > 450:
            posicaoYPersona = 450

        if not pausado:
            posicaoXlanca = posicaoXlanca - velocidadelanca
        if posicaoXlanca < -125:
            pygame.mixer.Sound.play(lancaSound)
            posicaoXlanca = 800
            pontos = pontos + 1
            velocidadelanca = velocidadelanca + 1

            novo_nivel = obter_nivel(pontos)
            if novo_nivel != nivel_atual:
                nivel_atual = novo_nivel
                voz.say("Nivel " + novo_nivel)
                voz.runAndWait()

            velocidadeFundo = velocidadeFundo + 0.3
            posicaoYlanca = random.randint(0, 1000)

        if not pausado:
            posicaoXNuvem -= velocidadeNuvem

        if posicaoXNuvem < -120:
            posicaoXNuvem = 1000
            posicaoYNuvem = random.randint(0, 200)

        tela.fill(branco)
        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))
        if not pausado:
            fundoMov1 -= velocidadeFundo
            fundoMov2 -= velocidadeFundo
        if fundoMov1 < -1000:
            fundoMov1 = 1000
        elif fundoMov2 < -1000:
            fundoMov2 = 1000

        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))

        if not pausado:
            fase_sol += SOL_VELOCIDADE
        desenhar_sol(tela, fase_sol)

        tela.blit(nuvem, (posicaoXNuvem, posicaoYNuvem))
        velocidadeNuvem = random.randint(1, 5)
        tela.blit(dragon, (posicaoXPersona, posicaoYPersona))
        tela.blit(lanca, (posicaoXlanca, posicaoYlanca))

        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (700, 15))

        nivel = obter_nivel(pontos)
        textoNivel = fonteMenu.render("Nivel: " + nivel, True, branco)
        tela.blit(textoNivel, (700, 40))

        textoAjuda = fonteAjuda.render("Press Space to Pause Game", True, branco)
        tela.blit(textoAjuda, (10, 10))

        if pausado:
            textoPause = fontePause.render("PAUSE", True, branco)
            rectPause = textoPause.get_rect(center=(500, 350))
            tela.blit(textoPause, rectPause)

        hbDragonX = posicaoXPersona + DRAGON_HB_OX
        hbDragonY = posicaoYPersona + DRAGON_HB_OY
        hblancaX = posicaoXlanca + lanca_HB_OX
        hblancaY = posicaoYlanca + lanca_HB_OY

        pixelsPersonaX = list(range(hbDragonX, hbDragonX + DRAGON_HB_W))
        pixelsPersonaY = list(range(hbDragonY, hbDragonY + DRAGON_HB_H))
        pixelslancaX = list(range(hblancaX, hblancaX + lanca_HB_W))
        pixelslancaY = list(range(hblancaY, hblancaY + lanca_HB_H))
        colisaoX = len(set(pixelsPersonaX).intersection(set(pixelslancaX))) > 0
        colisaoY = len(set(pixelsPersonaY).intersection(set(pixelslancaY))) > 0
        if colisaoX and colisaoY:
            escreverDados(nome, pontos)
            dead(pontos)

        pygame.display.update()
        relogio.tick(60)


def dead(pontos_atual):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    nome_max, pontos_max, _ = maior_pontuador()
    larguraButtonStart = 150
    alturaButtonStart = 40

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    jogar()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))
        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        textoPontuacao = fonteMenu.render(f"Sua Pontuação: {pontos_atual}", True, branco)
        tela.blit(textoPontuacao, (400, 580))

        textoMax = fonteMenu.render(f"Pontuação Máxima: {nome_max} - {pontos_max}", True, branco)
        tela.blit(textoMax, (400, 605))

        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart = 40
    amarelo = (255, 220, 0)
    laranja = (255, 160, 0)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 18))

        texto = fonteMenu.render(f"The Best: {nome_maior}  {maior_pontos} pts  {dataJogada}", True, branco)
        tela.blit(texto, (480, 15))

        painel = pygame.Surface((560, 340), pygame.SRCALPHA)
        pygame.draw.rect(painel, (0, 0, 0, 150), (0, 0, 560, 340), border_radius=18)
        tela.blit(painel, (220, 180))

        txtBv = fonteBoasVindas.render(f"Bem-vindo, {nome}!", True, amarelo)
        tela.blit(txtBv, (240, 195))

        pygame.draw.line(tela, laranja, (240, 238), (760, 238), 2)

        txtHist = fonteTitulo.render("Historia", True, laranja)
        tela.blit(txtHist, (240, 248))

        tela.blit(fonteTexto.render("Voce e um dragao corajoso voando pelos ceus.", True, branco), (240, 275))
        tela.blit(fonteTexto.render("Lancas inimigas sao disparadas em sua direcao.", True, branco), (240, 296))
        tela.blit(fonteTexto.render("Desvie de tudo e prove que e o mestre dos dragoes!", True, branco), (240, 317))

        pygame.draw.line(tela, laranja, (240, 345), (760, 345), 2)

        txtCtrl = fonteTitulo.render("Controles", True, laranja)
        tela.blit(txtCtrl, (240, 355))

        tela.blit(fonteTexto.render("Seta para Cima    ->  Mover o dragao para cima", True, branco), (240, 382))
        tela.blit(fonteTexto.render("Seta para Baixo   ->  Mover o dragao para baixo", True, branco), (240, 403))
        tela.blit(fonteTexto.render("Espaco            ->  Pausar / Retomar o jogo", True, branco), (240, 424))
        tela.blit(fonteTexto.render("ESC               ->  Fechar o jogo", True, branco), (240, 445))

        pygame.display.update()
        relogio.tick(60)


start()
