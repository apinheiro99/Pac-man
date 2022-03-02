import pygame
from abc import ABC, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode ((800, 600), 0)
fonte = pygame.font.SysFont("arial", 24, True, False)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0,255, 0)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
CIANO = (0, 255,255)
VELOCIDADE = 1
ACIMA = 1
ABAIX0 = 2
DIREITA = 3
ESQUERDA = 4

class ElementoJogo(ABC):
    
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(ABC):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass

class Cenario(ElementoJogo):
    def __init__(self, tamanho, pacman) -> None:
        self.pacman = pacman
        self.moviveis = [pacman]
        self.tamanho = tamanho
        self.pontos = 0
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, objeto):
        self.moviveis.append(objeto)

    def pintar_pontos(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render(f"Score: {self.pontos}", True, AMARELO)
        tela.blit(img_pontos, (pontos_x,50))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half, y + half), 
                        self.tamanho // 10, 0)

    def pintar(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_pontos(tela)

    def get_direcoes (self, linha, coluna):
        direcoes = []

        if self.matriz[linha - 1][coluna] != 2:
            direcoes.append(ACIMA)
        if self.matriz[linha + 1][coluna] != 2:
            direcoes.append(ABAIX0)        
        if self.matriz[linha][coluna + 1] != 2:
            direcoes.append(DIREITA)
        if self.matriz[linha][coluna - 1] != 2:
            direcoes.append(ESQUERDA)

        return direcoes

    def calcular_regras(self):
        # direcoes = self.get_direcoes(self.fantasma.linha, self.fantasma.coluna)
        # if len(direcoes) >= 3:
        #     self.fantasma.esquina(direcoes)

        # col = self.pacman.coluna_intencao
        # lin = self.pacman.linha_intencao
        # if 0 <= col < 28 and 0 <= lin < 29:
        #     if self.matriz[lin][col] != 2:
        #         self.pacman.aceitar_movimento()
        #         if self.matriz[lin][col] == 1:
        #             self.pontos += 1
        #             self.matriz[lin][col] = 0

        # col = self.fantasma.coluna_intencao
        # lin = self.fantasma.linha_intencao
        # if 0 <= col < 28 and 0 <= lin < 29 and self.matriz[lin][col] != 2:
        #     self.fantasma.aceitar_movimento()
        # else:
        #     self.fantasma.recusar_movimento(direcoes)

        for movivel in self.moviveis:
            col = movivel.coluna
            lin = movivel.linha
            col_intencao = movivel.coluna_intencao
            lin_intencao = movivel.linha_intencao

            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)

            if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                    self.matriz[lin_intencao][col_intencao] != 2:
                movivel.aceitar_movimento()
                if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                    self.pontos += 1
                    self.matriz[lin][col] = 0
            else:
                movivel.recusar_movimento(direcoes)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()

class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho) -> None:
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y

        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar (self, tela):
        # Desenha o corpo do Pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # Desenho da boca
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # Desenho do olho
        olho_x = self.centro_x + int(self.raio / 3)
        olho_y = self.centro_y - int(self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = VELOCIDADE
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -VELOCIDADE
                elif e.key == pygame.K_UP:
                    self.vel_y = -VELOCIDADE
                elif e.key == pygame.K_DOWN:
                    self.vel_y = VELOCIDADE

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

    def processar_eventos_mouse(self, eventos):
        # delay = 100
        for e in eventos:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                # self.coluna = (mouse_x - self.centro_x) / delay
                # self.linha = (mouse_y - self.centro_y) / delay
                # self.coluna = (mouse_x - self.raio) // self.tamanho
                # self.linha = (mouse_y - self.raio) // self.tamanho
                self.coluna = mouse_x // self.tamanho
                self.linha = mouse_y // self.tamanho

class Fantasma(ElementoJogo, Movivel):

    def __init__(self, tamanho, fantasma) -> None:
        self.coluna = 6
        self.linha = 1
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.direcao = ABAIX0
        self.velocidade = 1
        self.tamanho = tamanho
        self.fantasma, self.cor = self.seleciona_fantasma(fantasma)

    def seleciona_fantasma(self, fantasma):
        if fantasma == "blinky":
            matriz = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,2,2,1,1,1,1,2,2,0,0,0,0],
            [0,0,0,1,1,2,2,2,2,1,1,2,2,2,2,0,0,0],
            [0,0,0,1,1,2,2,3,3,1,1,2,2,3,3,0,0,0],
            [0,0,1,1,1,2,2,3,3,1,1,2,2,3,3,1,0,0],
            [0,0,1,1,1,1,2,2,1,1,1,1,2,2,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,0],
            [0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ]
            cor = [PRETO, VERMELHO, BRANCO, VERDE]
        elif fantasma == "inky":
            matriz = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,2,2,1,1,1,1,2,2,0,0,0,0],
            [0,0,0,1,1,2,2,2,2,1,1,2,2,2,2,0,0,0],
            [0,0,0,1,1,2,2,3,3,1,1,2,2,3,3,0,0,0],
            [0,0,1,1,1,2,2,3,3,1,1,2,2,3,3,1,0,0],
            [0,0,1,1,1,1,2,2,1,1,1,1,2,2,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,0],
            [0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ]
            cor = [PRETO, CIANO, BRANCO, VERDE]
        elif fantasma == "clyde":
            matriz = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,2,2,1,1,1,1,2,2,0,0,0,0],
            [0,0,0,1,1,2,2,2,2,1,1,2,2,2,2,0,0,0],
            [0,0,0,1,1,2,2,3,3,1,1,2,2,3,3,0,0,0],
            [0,0,1,1,1,2,2,3,3,1,1,2,2,3,3,1,0,0],
            [0,0,1,1,1,1,2,2,1,1,1,1,2,2,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,0],
            [0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ]
            cor = [PRETO, LARANJA, BRANCO, VERDE]
        elif fantasma == "pinky":
            matriz = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,2,2,1,1,1,1,2,2,0,0,0,0],
            [0,0,0,1,1,2,2,2,2,1,1,2,2,2,2,0,0,0],
            [0,0,0,1,1,2,2,3,3,1,1,2,2,3,3,0,0,0],
            [0,0,1,1,1,2,2,3,3,1,1,2,2,3,3,1,0,0],
            [0,0,1,1,1,1,2,2,1,1,1,1,2,2,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,0],
            [0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ]
            cor = [PRETO, ROSA, BRANCO, VERDE]
        return matriz, cor

    def pintar(self, tela):
        fatia = self.tamanho // 18

        x = int(self.coluna * self.tamanho)
        y = int(self.linha * self.tamanho)

        for numero_linha, linha in enumerate(self.fantasma):
            for numero_coluna, coluna in enumerate(linha):
                x_inicio = int(x + (numero_coluna * fatia))
                y_inicio = int(y + (numero_linha * fatia))

                cor = self.cor[coluna]

                pygame.draw.rect(tela, cor, (x_inicio + fatia, y_inicio + fatia, fatia, fatia), 0)

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIX0:
            self.linha_intencao += self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade 
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade 

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)
        
    def processar_eventos(self, eventos):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Fantasma(size, "blinky")
    inky = Fantasma(size, "inky")
    clyde = Fantasma(size, "clyde")
    pinky = Fantasma(size, "pinky")
    cenario = Cenario(size,pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        # Calcular as regras
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()
        
        # Pintar a tela
        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Captura os eventos
        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)
