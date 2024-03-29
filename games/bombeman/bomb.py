import pygame

LIFE_TIME = 90
BLAST_TIME = 15
BOMB_SIZE = 20

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blast_img = pygame.image.load(f'./images/blust_1.png')
        self.blast_img.convert()
        self.rect = self.blast_img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.blast_img = pygame.transform.rotozoom(self.blast_img, 0, 120 / self.rect.width)
        self.counter = LIFE_TIME
        self.img = pygame.image.load(f'./images/bomb_1.png')        
        self.set_image()
        self.ghost = False  

    def draw(self, surface):
        if self.counter < 0:
            self.rect.x = self.x - 40
            self.rect.y = self.y - 40
            surface.blit(self.blast_img, self.rect)
        else:
            self.rect.x = self.x
            self.rect.y = self.y
            surface.blit(self.img, self.rect)          
    
    def tick(self):
        self.counter -= 1
        return self.counter > -BLAST_TIME  

    def check_hit(self, brick):
        boom = self.counter < 0 
        hit = (self.x == brick.x ) and (self.y == brick.y)
        hit_bottom = (self.x == brick.x ) and (self.y == brick.y - 40)
        hit_top = (self.x == brick.x) and (self.y == brick.y + 40)
        hit_left = (self.x == brick.x - 40) and (self.y == brick.y)
        hit_right = (self.x == brick.x + 40) and (self.y == brick.y)
        hit_top_right = (self.x == brick.x + 40) and (self.y == brick.y + 40)
        hit_top_left = (self.x == brick.x - 40) and (self.y == brick.y + 40)
        hit_bottom_right = (self.x == brick.x + 40) and (self.y == brick.y - 40)
        hit_bottom_left = (self.x == brick.x - 40) and (self.y == brick.y - 40)
        return boom and (hit or hit_top or hit_bottom or hit_left or hit_right or hit_top_right or hit_top_left or hit_bottom_right or hit_bottom_left)
    
    def set_image(self):  
        self.img.convert()
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.img = pygame.transform.rotozoom(self.img, 0, 40 / self.rect.width)

class GhostBomb(Bomb):
    def __init__(self, surface, x, y):
        super().__init__(x, y)   
        self.surface = surface
        self.img = pygame.image.load(f'./images/bomb_2.png')
        self.ghost = True    
        self.set_image()