import pygame
import random
from pygame.sprite import Sprite
from utils import resource_path

class Alien(Sprite):

    def __init__(self,ai_settings,screen):
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 使用工具函数加载图像，兼容开发环境和打包环境
        self.image = pygame.image.load(resource_path('images/alien.bmp'))
        self.rect =self.image.get_rect()

        # 随机生成外星人的初始位置（从屏幕上方出现）
        self.rect.x = random.randint(0, ai_settings.screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -self.rect.height)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # 为每个外星人设置独立的移动方向和速度
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([0.5, 1])
        self.speed_factor = random.uniform(ai_settings.alien_speed_factor * 0.5, ai_settings.alien_speed_factor * 1.5)
    
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False
    
    def update(self, ship=None):
        # 随机改变方向（1%的概率）
        if random.randint(0, 100) < 1:
            self.direction_x *= -1
        if random.randint(0, 100) < 1:
            self.direction_y = random.choice([0.5, 1])
        
        # 如果提供了飞船，尝试向飞船方向移动
        if ship:
            # 20%的概率向飞船方向调整
            if random.randint(0, 100) < 20:
                if self.x < ship.rect.centerx:
                    self.direction_x = 1
                elif self.x > ship.rect.centerx:
                    self.direction_x = -1
                
                if self.y < ship.rect.centery:
                    self.direction_y = 1
                elif self.y > ship.rect.centery:
                    self.direction_y = 0.5
        
        # 更新位置
        self.x += (self.speed_factor * self.direction_x)
        self.y += (self.speed_factor * self.direction_y)
        
        # 边界检测
        if self.check_edges():
            self.direction_x *= -1
        
        self.rect.x = self.x
        self.rect.y = self.y