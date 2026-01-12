import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    def __init__(self, ai_settings,screen, ship):
        super(Bullet,self).__init__()   #继承类
        self.screen = screen
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx  #先绘画矩形，再定位
        self.rect.top = ship.rect.top
        #小数点表示子弹的位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.screen_factor =ai_settings.bullet_speed_factor
    def update(self):
        self.y -=self.screen_factor
        self.rect.y =self.y  #变量传递
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color, self.rect)
    
