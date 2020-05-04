import pygame
from random import *

class Small_virus(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("resources/image/virus1.png").convert_alpha(), (40, 45))
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = randint(0,self.width-self.rect.width),randint((-1*self.height),0)
        self.active = True
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 1

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else :
            self.reset()


    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint((-1 * self.height), 0)
        self.active = True


class Mid_virus(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("resources/image/virus2.png").convert_alpha(), (60, 65))
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = randint(0,self.width-self.rect.width),randint((-2*self.height),0)
        self.active = True
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 2

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else :
            self.reset()


    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint((-2 * self.height), 0)
        self.active = True


class Big_virus(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("resources/image/virus3.png").convert_alpha(), (80, 85))
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = randint(0,(self.width-self.rect.width)//2),randint((-3*self.height),0)
        self.active = True
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 3

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else :
            self.reset()


    def reset(self):
        self.rect.left, self.rect.top = randint(0, (self.width - self.rect.width) // 2), randint((-3 * self.height), 0)
        self.active = True
