import pygame
from random import randint, choice, random

class Duck(pygame.sprite.Sprite):

    def __init__(self,speed, x, y):
        super().__init__()

        # PARAMETRY ORGANIZMU
        self.speed = speed
        self.sense = 1

        # Prawdopodobieńśtwo, że kaczucha zmieni kierunek
        self.change_dir_probability = 0.3

        # GRAFIKI DO ANIMACJI
        self.frames = {
        'front': [pygame.image.load('graphics/duckies/front.png').convert_alpha()],
        'back': [pygame.image.load('graphics/duckies/back.png').convert_alpha()],
        'down': [
            pygame.image.load('graphics/duckies/front-walk-1.png').convert_alpha(),
            pygame.image.load('graphics/duckies/front-walk-2.png').convert_alpha(),
            pygame.image.load('graphics/duckies/front-walk-3.png').convert_alpha(),
            pygame.image.load('graphics/duckies/front-walk-4.png').convert_alpha(),
        ],
        'up': [
            pygame.image.load('graphics/duckies/back-walk-1.png').convert_alpha(),
            pygame.image.load('graphics/duckies/back-walk-2.png').convert_alpha(),
            pygame.image.load('graphics/duckies/back-walk-3.png').convert_alpha(),
            pygame.image.load('graphics/duckies/back-walk-4.png').convert_alpha(),
        ],
        'right': [
            pygame.image.load('graphics/duckies/side-walk-1.png').convert_alpha(),
            pygame.image.load('graphics/duckies/side-walk-2.png').convert_alpha(),
            pygame.image.load('graphics/duckies/side-walk-3.png').convert_alpha(),
            pygame.image.load('graphics/duckies/side-walk-4.png').convert_alpha(),
        ],
        }
        self.frames['left'] = [pygame.transform.flip(img, True, False) for img in self.frames['right']]

        # ustawienie stanu animacji
        self.directions = {'down': (0, 1), 'up': (0, -1), 'right': (1, 0), 'left': (-1,0), 'front': (0,0)}
        self.duck_direction = 'front'
        self.duck_frame_idx = 0

        # Pygame owe rzeczy
        self.image = self.frames['front'][0]
        self.rect = self.image.get_rect(midbottom = (x, y))

    def animation_state(self, next_dir):
        """
        funkcja ustawia, która z grafik animacji powinna zostać w danej klatce wyświetlona
        """
        if next_dir != self.duck_direction: 
            self.duck_frame_idx = 0
            self.duck_direction = next_dir

        # chcemu żeby nowa grafika się pojawiała co kilka klatek
        self.duck_frame_idx += 0.2
        if self.duck_frame_idx >= len(self.frames[self.duck_direction]): self.duck_frame_idx = 0

        self.image = self.frames[self.duck_direction][int(self.duck_frame_idx)]



    def update(self):
        """
        funkcja modyfikująca współrzędne obiektu
        """
        # ustawienie nowego kierunku
        next_dir = self.duck_direction
        if random() < self.change_dir_probability:
            next_dir = choice(list(self.directions.keys()))
        self.animation_state(next_dir)

        # poruszamy się o self.speed pixli w danym kierunku
        # nowa pozycja x-owa += kierunke[0] * speed
        # możliwe kierunki -> (-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)
        self.rect.x += self.directions[next_dir][0] * self.speed
        if self.rect.left < 200: self.rect.right = 1000
        if self.rect.right > 1000: self.rect.left = 200

        # tak samo ja wyżej tylko, że dla y
        self.rect.y += self.directions[next_dir][1] * self.speed
        if self.rect.top < 0: self.rect.bottom = 800
        if self.rect.bottom > 800: self.rect.top = 0

    
    def update_energy(self: object, energy: float) -> float:
        '''
        Koszt energii w jednej jednostce czasu, jaki ponosi
        organizm. W przypadku jeśli spadnie to zera to
        kaczucha umiera.
        energy = enrgy - (speed^2 * sense)
        '''
        self.energy -= self.speed**2 * (self.sense / 0.5)