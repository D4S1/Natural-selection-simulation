import pygame
from random import randint, choice, random


class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('graphics/l3.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.65)
        self.rect = self.image.get_rect(midbottom=(x, y))
