import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("resources/image/bullet.png").convert_alpha(),(10,20))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.active = True
        self.speed = 8
        self.rect.left -= self.rect.width//2
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self,position):
        self.rect.left,self.rect.top = position
        self.rect.left -= self.rect.width //2
        self.active = True

