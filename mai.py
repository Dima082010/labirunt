import pygame
pygame.init()
import os

def fila_path(file_name):
    folder = os.path.abspath(__file__ + '/..')
    path = os.path.join(folder, file_name)
    return path

WIN_WIDTH = 1200
WIN_HEIGHT = 700
FPS = 40

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

fon = pygame.image.load(fila_path(r"images\turma.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

class Game_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_name):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(fila_path(image_name))
        self.image = pygame.transform.scale(self.image, (width, height))

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Game_sprite(5, 6, 50, 70, r'images\Luffy.png')
enemy = Game_sprite(1100, 500, 50, 70, r'images\Mochi.webp')
finish = Game_sprite(500, 300, 40, 60, r'images\frukt.png')


lvl = 1
game = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if lvl == 1:
        window.blit(fon, (0, 0))
        player.show()
        enemy.show()
        finish.show()

    clock.tick(FPS)
    pygame.display.update()