import pygame
from utils import resource_path
class Ship():
    def __init__(self, ai_settings,screen):
        self.screen = screen
        self.ai_settings = ai_settings
        # 使用工具函数加载图像，兼容开发环境和打包环境
        self.image = pygame.image.load(resource_path('images/spaceship2.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom 
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom :
            self.bottom += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom
       
    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom