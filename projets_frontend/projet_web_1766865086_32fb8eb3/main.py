import pygame
import random
import sys

# Constantes
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2, 50, 50)
        self.vies = 3

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5

class Ennemi(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, WIDTH), random.randint(0, HEIGHT), 50, 50)

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)

class Piece(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, WIDTH), random.randint(0, HEIGHT), 50, 50)

class Plateforme(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, WIDTH), random.randint(0, HEIGHT), 200, 50)

class Boss(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2, 100, 100)

def afficher_texte(texte, x, y, taille, couleur):
    police = pygame.font.SysFont('Arial', taille)
    texte = police.render(texte, True, couleur)
    ecran.blit(texte, (x, y))

def jeu():
    pygame.init()
    global ecran
    ecran = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Jeu de plateforme')
    clock = pygame.time.Clock()

    player = Player()
    ennemis = [Ennemi() for _ in range(5)]
    pièces = [Piece() for _ in range(5)]
    plateformes = [Plateforme() for _ in range(5)]
    boss = Boss()

    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.collidepoint(event.pos):
                    score += 1
                    player.vies += 1

        ecran.fill(WHITE)
        player.move()
        for ennemi in ennemis:
            ennemi.move()
            if ennemi.colliderect(player):
                player.vies -= 1
                ennemis.remove(ennemi)
        for pièce in pièces:
            if pièce.colliderect(player):
                score += 1
                pièces.remove(pièce)
        for plateforme in plateformes:
            plateforme.move()
            if plateforme.colliderect(player):
                player.vies -= 1
                plateformes.remove(plateforme)
        boss.move()
        if boss.colliderect(player):
            player.vies -= 1

        afficher_texte(f'Score : {score}', 10, 10, 24, BLACK)
        afficher_texte(f'Vies : {player.vies}', 10, 40, 24, BLACK)
        pygame.draw.rect(ecran, RED, player)
        for ennemi in ennemis:
            pygame.draw.rect(ecran, BLUE, ennemi)
        for pièce in pièces:
            pygame.draw.rect(ecran, GREEN, pièce)
        for plateforme in plateformes:
            pygame.draw.rect(ecran, WHITE, plateforme)
        pygame.draw.rect(ecran, RED, boss)
        pygame.display.flip()
        clock.tick(60)

        if player.vies <= 0:
            print(f'Vous avez perdu ! Votre score : {score}')
            break

        if len(ennemis) == 0 and len(pièces) == 0 and len(plateformes) == 0:
            print(f'Vous avez gagné ! Votre score : {score}')
            break

def main():
    pygame.init()
    global ecran
    ecran = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Jeu de plateforme')
    clock = pygame.time.Clock()

    jeu()

    pygame.quit()

if __name__ == "__main__":
    main()
