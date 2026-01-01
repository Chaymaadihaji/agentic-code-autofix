import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Création de la fenêtre
win = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.Rect):
    def __init__(self):
        super().__init__(100, 100, 50, 50)
        self.speed = 5
        self.health = 100

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

class Enemy(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), 50, 50)
        self.speed = 2

    def move(self):
        self.x += self.speed

        if self.x < 0 or self.x > WIDTH - self.width:
            self.speed *= -1

class Coin(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20)

class Platform(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

class World:
    def __init__(self):
        self.platforms = [Platform(0, HEIGHT - 50, WIDTH, 50), Platform(WIDTH / 2, HEIGHT / 2, 100, 50)]
        self.enemies = [Enemy()]
        self.coins = [Coin()]
        self.player = Player()

    def update(self):
        for enemy in self.enemies:
            enemy.move()

        for coin in self.coins:
            if coin.colliderect(self.player):
                self.coins.remove(coin)
                print("Vous avez trouvé une pièce !")

        if self.player.health <= 0:
            print("Vous avez perdu !")
            pygame.quit()
            sys.exit()

class Game:
    def __init__(self):
        self.world = World()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.world.player.move(-self.world.player.speed, 0)
            if keys[pygame.K_RIGHT]:
                self.world.player.move(self.world.player.speed, 0)
            if keys[pygame.K_UP]:
                self.world.player.move(0, -self.world.player.speed)
            if keys[pygame.K_DOWN]:
                self.world.player.move(0, self.world.player.speed)

            self.world.update()

            win.fill(BLUE)
            for platform in self.world.platforms:
                pygame.draw.rect(win, GREEN, platform)
            for enemy in self.world.enemies:
                pygame.draw.rect(win, RED, enemy)
            for coin in self.world.coins:
                pygame.draw.rect(win, WHITE, coin)
            pygame.draw.rect(win, (0, 0, 0), self.world.player)

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
