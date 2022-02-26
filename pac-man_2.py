import pygame

pygame.init()

screen = pygame.display.set_mode ((800, 600), 0)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

class Pacman:
    def __init__(self) -> None:
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = 800 // 30
        self.vel_x = 1
        self.vel_y = 1
        self.raio = self.tamanho // 2

    def calcular_regras(self):
        self.coluna = self.coluna + self.vel_x
        self.linha = self.linha + self.vel_y

        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

        if self.centro_x + self.raio > 800:
            self.vel_x = -self.vel_x
        if self.centro_x - self.raio < 0:
            self.vel_x = -self.vel_x

        if self.centro_y + self.raio > 600:
            self.vel_y = -self.vel_y
        if self.centro_y - self.raio < 0:
            self.vel_y = -self.vel_y

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

if __name__ == "__main__":
    pacman = Pacman()

    while True:
        # Calcular as regras
        pacman.calcular_regras()

        # Pintar a tela
        screen.fill(PRETO)
        pacman.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Captura os eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
