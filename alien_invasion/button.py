import pygame.font
class Button():
    def __init__(self,ai_settings,screen, msg, position=None):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.height = 60  # 固定高度
        # 不使用背景色，与游戏屏幕一致
        self.button_color = ai_settings.bg_color
        self.text_color = (0, 0, 0)  # 文字颜色保持黑色
        # 使用系统中文黑体字体，支持中文显示
        self.font = pygame.font.SysFont("SimHei", 48)
        self.msg = msg
        
        # 初始化时渲染文字，计算按钮宽度
        self._prep_msg()
        
        # 根据传入的位置设置按钮位置，默认为居中
        if position is None:
            self.rect.center = self.screen_rect.center
        else:
            self.rect.x, self.rect.y = position
    
    def _prep_msg(self):
        """渲染文字并设置按钮宽度，宽度根据文字长度自动调整"""
        # 渲染文字
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        
        # 根据文字宽度设置按钮宽度，添加适当的内边距
        padding = 40  # 左右各20像素的内边距
        self.width = self.msg_image_rect.width + padding
        # 创建按钮矩形
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 确保文字居中
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        # 如果是暂停按钮，绘制两条黑色竖线
        if self.msg == "暂停":
            # 绘制按钮区域背景色，与游戏屏幕一致
            self.screen.fill(self.button_color, self.rect)
            # 绘制第一条竖线
            line1_rect = pygame.Rect(0, 0, 10, self.height - 20)
            line1_rect.centerx = self.rect.centerx - 15
            line1_rect.centery = self.rect.centery
            pygame.draw.rect(self.screen, (0, 0, 0), line1_rect)
            # 绘制第二条竖线
            line2_rect = pygame.Rect(0, 0, 10, self.height - 20)
            line2_rect.centerx = self.rect.centerx + 15
            line2_rect.centery = self.rect.centery
            pygame.draw.rect(self.screen, (0, 0, 0), line2_rect)
        else:
            # 其他按钮正常绘制
            # 绘制背景
            self.screen.fill(self.button_color, self.rect)
            # 渲染文字
            # 重新渲染文字以确保最新
            self._prep_msg()
            self.screen.blit(self.msg_image, self.msg_image_rect)