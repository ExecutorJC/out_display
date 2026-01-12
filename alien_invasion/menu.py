import pygame.font
import pygame

class Menu():
    """游戏菜单类"""
    
    def __init__(self, ai_settings, screen):
        """初始化菜单属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        
        # 菜单按钮属性
        self.button_color = (0, 255, 0)  # 主菜单按钮颜色保持不变
        self.settings_bg_color = (173, 216, 230)  # 设置界面背景色为浅蓝色
        self.text_color = (0, 0, 0)  # 字体颜色改为黑色
        self.number_color = (255, 0, 0)  # 数字颜色为红色
        self.number_outline_color = (0, 0, 0)  # 数字外框颜色为黑色
        self.selected_color = (0, 255, 0)  # 选中状态的颜色
        # 使用系统中文黑体字体，支持中文显示
        self.font = pygame.font.SysFont("SimHei", 48)
        self.small_font = pygame.font.SysFont("SimHei", 36)  # 用于数字显示的小字体
        
        # 创建菜单项
        self.create_buttons()
        
        # 菜单状态
        self.game_paused = False
        self.show_settings = False
        
        # 倒计时相关属性
        self.countdown_active = False
        self.countdown_time = 3
        self.countdown_start_time = 0
        
        # 设置菜单中的输入状态
        self.selected_setting = None  # 当前选中的设置项
        self.editing = False  # 是否处于编辑状态
        self.input_text = ""  # 输入的文本
        
        # 光标闪烁相关属性
        self.cursor_visible = True  # 光标是否可见
        self.cursor_blink_interval = 500  # 光标闪烁间隔（毫秒）
        self.last_cursor_blink = pygame.time.get_ticks()  # 上次光标闪烁时间
        
    def create_buttons(self):
        """创建菜单项"""
        # 主菜单按钮
        self.resume_button = self._create_button("继续游戏", self.screen_rect.centery - 100)
        self.settings_button = self._create_button("设置", self.screen_rect.centery)
        self.quit_button = self._create_button("退出游戏", self.screen_rect.centery + 100)
        
        # 设置菜单
        # 飞船速度设置
        self.ship_speed_label = self._create_label("飞船速度:", self.screen_rect.centery - 150)
        self.ship_speed_value = self._create_value_label("{:.1f}".format(self.ai_settings.ship_speed_factor), 
                                                       self.screen_rect.centery - 150, 150)
        
        # 外星人速度设置
        self.alien_speed_label = self._create_label("外星人速度:", self.screen_rect.centery - 50)
        self.alien_speed_value = self._create_value_label("{:.1f}".format(self.ai_settings.alien_speed_factor), 
                                                        self.screen_rect.centery - 50, 150)
        
        # 子弹速度设置
        self.bullet_speed_label = self._create_label("子弹速度:", self.screen_rect.centery + 50)
        self.bullet_speed_value = self._create_value_label("{:.1f}".format(self.ai_settings.bullet_speed_factor), 
                                                        self.screen_rect.centery + 50, 150)
        
        # 返回按钮
        self.back_button = self._create_button("返回", self.screen_rect.centery + 150)
    
    def _create_button(self, text, y_position):
        """创建单个按钮"""
        button_rect = pygame.Rect(0, 0, 400, 50)
        button_rect.centerx = self.screen_rect.centerx
        button_rect.centery = y_position
        
        button_image = self.font.render(text, True, self.text_color, self.button_color)
        button_image_rect = button_image.get_rect()
        button_image_rect.center = button_rect.center
        
        return {
            "rect": button_rect,
            "image": button_image,
            "image_rect": button_image_rect,
            "text": text
        }
    
    def _create_label(self, text, y_position):
        """创建设置项标签"""
        label_image = self.font.render(text, True, self.text_color)
        label_rect = label_image.get_rect()
        label_rect.centerx = self.screen_rect.centerx - 100
        label_rect.centery = y_position
        
        return {
            "image": label_image,
            "rect": label_rect
        }
    
    def _create_value_label(self, text, y_position, x_offset):
        """创建设置项数值标签"""
        # 首先渲染黑色外框
        outline_image = self.small_font.render(text, True, self.number_outline_color)
        # 然后渲染红色数字
        value_image = self.small_font.render(text, True, self.number_color)
        
        value_rect = value_image.get_rect()
        value_rect.centerx = self.screen_rect.centerx + x_offset
        value_rect.centery = y_position
        
        return {
            "outline_image": outline_image,
            "image": value_image,
            "rect": value_rect
        }
    
    def _create_small_button(self, text, y_position, x_offset):
        """创建增减按钮"""
        button_rect = pygame.Rect(0, 0, 50, 50)
        button_rect.centerx = self.screen_rect.centerx + x_offset
        button_rect.centery = y_position
        
        button_image = self.font.render(text, True, self.text_color, self.button_color)
        button_image_rect = button_image.get_rect()
        button_image_rect.center = button_rect.center
        
        return {
            "rect": button_rect,
            "image": button_image,
            "image_rect": button_image_rect,
            "text": text
        }
    
    def update_buttons(self):
        """更新设置项数值显示"""
        # 更新飞船速度显示
        ship_speed_text = "{:.1f}".format(self.ai_settings.ship_speed_factor)
        self.ship_speed_value["outline_image"] = self.small_font.render(ship_speed_text, True, self.number_outline_color)
        self.ship_speed_value["image"] = self.small_font.render(ship_speed_text, True, self.number_color)
        
        # 更新外星人速度显示
        alien_speed_text = "{:.1f}".format(self.ai_settings.alien_speed_factor)
        self.alien_speed_value["outline_image"] = self.small_font.render(alien_speed_text, True, self.number_outline_color)
        self.alien_speed_value["image"] = self.small_font.render(alien_speed_text, True, self.number_color)
        
        # 更新子弹速度显示
        bullet_speed_text = "{:.1f}".format(self.ai_settings.bullet_speed_factor)
        self.bullet_speed_value["outline_image"] = self.small_font.render(bullet_speed_text, True, self.number_outline_color)
        self.bullet_speed_value["image"] = self.small_font.render(bullet_speed_text, True, self.number_color)
    
    def draw_menu(self):
        """绘制菜单"""
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.show_settings:
            # 绘制浅蓝色背景的设置面板
            settings_panel = pygame.Rect(0, 0, 600, 400)
            settings_panel.center = self.screen_rect.center
            self.screen.fill(self.settings_bg_color, settings_panel)
            
            # 绘制飞船速度设置
            self.screen.blit(self.ship_speed_label["image"], self.ship_speed_label["rect"])
            
            # 绘制数值外框
            self.screen.blit(self.ship_speed_value["outline_image"], (self.ship_speed_value["rect"].x - 1, self.ship_speed_value["rect"].y - 1))
            self.screen.blit(self.ship_speed_value["outline_image"], (self.ship_speed_value["rect"].x + 1, self.ship_speed_value["rect"].y + 1))
            self.screen.blit(self.ship_speed_value["outline_image"], (self.ship_speed_value["rect"].x - 1, self.ship_speed_value["rect"].y + 1))
            self.screen.blit(self.ship_speed_value["outline_image"], (self.ship_speed_value["rect"].x + 1, self.ship_speed_value["rect"].y - 1))
            
            # 更新光标闪烁状态
            current_time = pygame.time.get_ticks()
            if current_time - self.last_cursor_blink >= self.cursor_blink_interval:
                self.cursor_visible = not self.cursor_visible
                self.last_cursor_blink = current_time
            
            # 绘制选中状态
            if self.selected_setting == "ship_speed":
                # 绘制选中高亮框
                highlight_rect = self.ship_speed_value["rect"].copy()
                highlight_rect.inflate_ip(10, 10)  # 扩大10像素
                pygame.draw.rect(self.screen, self.selected_color, highlight_rect, 2)  # 绘制边框
                
                # 绘制输入文本
                if self.editing:
                    # 根据光标可见状态决定是否显示光标
                    input_text = self.input_text + ("|" if self.cursor_visible else " ")
                    input_image = self.small_font.render(input_text, True, self.number_color)
                    self.screen.blit(input_image, self.ship_speed_value["rect"])
                else:
                    self.screen.blit(self.ship_speed_value["image"], self.ship_speed_value["rect"])
            else:
                # 绘制红色数值
                self.screen.blit(self.ship_speed_value["image"], self.ship_speed_value["rect"])
            
            # 绘制外星人速度设置
            self.screen.blit(self.alien_speed_label["image"], self.alien_speed_label["rect"])
            
            # 绘制数值外框
            self.screen.blit(self.alien_speed_value["outline_image"], (self.alien_speed_value["rect"].x - 1, self.alien_speed_value["rect"].y - 1))
            self.screen.blit(self.alien_speed_value["outline_image"], (self.alien_speed_value["rect"].x + 1, self.alien_speed_value["rect"].y + 1))
            self.screen.blit(self.alien_speed_value["outline_image"], (self.alien_speed_value["rect"].x - 1, self.alien_speed_value["rect"].y + 1))
            self.screen.blit(self.alien_speed_value["outline_image"], (self.alien_speed_value["rect"].x + 1, self.alien_speed_value["rect"].y - 1))
            
            # 绘制选中状态
            if self.selected_setting == "alien_speed":
                # 绘制选中高亮框
                highlight_rect = self.alien_speed_value["rect"].copy()
                highlight_rect.inflate_ip(10, 10)  # 扩大10像素
                pygame.draw.rect(self.screen, self.selected_color, highlight_rect, 2)  # 绘制边框
                
                # 绘制输入文本
                if self.editing:
                    # 根据光标可见状态决定是否显示光标
                    input_text = self.input_text + ("|" if self.cursor_visible else " ")
                    input_image = self.small_font.render(input_text, True, self.number_color)
                    self.screen.blit(input_image, self.alien_speed_value["rect"])
                else:
                    self.screen.blit(self.alien_speed_value["image"], self.alien_speed_value["rect"])
            else:
                # 绘制红色数值
                self.screen.blit(self.alien_speed_value["image"], self.alien_speed_value["rect"])
            
            # 绘制子弹速度设置
            self.screen.blit(self.bullet_speed_label["image"], self.bullet_speed_label["rect"])
            
            # 绘制数值外框
            self.screen.blit(self.bullet_speed_value["outline_image"], (self.bullet_speed_value["rect"].x - 1, self.bullet_speed_value["rect"].y - 1))
            self.screen.blit(self.bullet_speed_value["outline_image"], (self.bullet_speed_value["rect"].x + 1, self.bullet_speed_value["rect"].y + 1))
            self.screen.blit(self.bullet_speed_value["outline_image"], (self.bullet_speed_value["rect"].x - 1, self.bullet_speed_value["rect"].y + 1))
            self.screen.blit(self.bullet_speed_value["outline_image"], (self.bullet_speed_value["rect"].x + 1, self.bullet_speed_value["rect"].y - 1))
            
            # 绘制选中状态
            if self.selected_setting == "bullet_speed":
                # 绘制选中高亮框
                highlight_rect = self.bullet_speed_value["rect"].copy()
                highlight_rect.inflate_ip(10, 10)  # 扩大10像素
                pygame.draw.rect(self.screen, self.selected_color, highlight_rect, 2)  # 绘制边框
                
                # 绘制输入文本
                if self.editing:
                    # 根据光标可见状态决定是否显示光标
                    input_text = self.input_text + ("|" if self.cursor_visible else " ")
                    input_image = self.small_font.render(input_text, True, self.number_color)
                    self.screen.blit(input_image, self.bullet_speed_value["rect"])
                else:
                    self.screen.blit(self.bullet_speed_value["image"], self.bullet_speed_value["rect"])
            else:
                # 绘制红色数值
                self.screen.blit(self.bullet_speed_value["image"], self.bullet_speed_value["rect"])
            
            # 绘制返回按钮
            self.screen.fill(self.button_color, self.back_button["rect"])
            self.screen.blit(self.back_button["image"], self.back_button["image_rect"])
        else:
            # 绘制主菜单
            self.screen.fill(self.button_color, self.resume_button["rect"])
            self.screen.blit(self.resume_button["image"], self.resume_button["image_rect"])
            
            self.screen.fill(self.button_color, self.settings_button["rect"])
            self.screen.blit(self.settings_button["image"], self.settings_button["image_rect"])
            
            self.screen.fill(self.button_color, self.quit_button["rect"])
            self.screen.blit(self.quit_button["image"], self.quit_button["image_rect"])
    
    def check_button_click(self, mouse_pos):
        """检查按钮点击事件"""
        if self.show_settings:
            # 检查设置菜单按钮
            
            # 飞船速度点击
            if self.ship_speed_value["rect"].collidepoint(mouse_pos):
                self.selected_setting = "ship_speed"
                self.editing = True
                self.input_text = "{:.1f}".format(self.ai_settings.ship_speed_factor)
            
            # 外星人速度点击
            elif self.alien_speed_value["rect"].collidepoint(mouse_pos):
                self.selected_setting = "alien_speed"
                self.editing = True
                self.input_text = "{:.1f}".format(self.ai_settings.alien_speed_factor)
            
            # 子弹速度点击
            elif self.bullet_speed_value["rect"].collidepoint(mouse_pos):
                self.selected_setting = "bullet_speed"
                self.editing = True
                self.input_text = "{:.1f}".format(self.ai_settings.bullet_speed_factor)
            
            # 返回按钮
            elif self.back_button["rect"].collidepoint(mouse_pos):
                # 保存当前设置
                self.save_setting()
                self.show_settings = False
        else:
            # 检查主菜单按钮
            if self.resume_button["rect"].collidepoint(mouse_pos):
                # 启动倒计时
                self.countdown_active = True
                self.countdown_start_time = pygame.time.get_ticks()
            elif self.settings_button["rect"].collidepoint(mouse_pos):
                self.show_settings = True
                self.update_buttons()
            elif self.quit_button["rect"].collidepoint(mouse_pos):
                return "quit"
        
        return None
    
    def handle_keyboard_input(self, event):
        """处理键盘输入"""
        # 只处理KEYDOWN事件
        if event.type == pygame.KEYDOWN:
            # 检查是否在设置界面并且有选中的设置项
            if self.show_settings and self.selected_setting is not None:
                # 如果还没有处于编辑状态，直接进入编辑状态
                if not self.editing:
                    self.editing = True
                    self.input_text = ""
                
                # 现在处理实际的键盘输入
                # 同时处理主键盘和数字键盘的回车键
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    # 保存设置并退出编辑状态
                    self.save_setting()
                elif event.key == pygame.K_ESCAPE:
                    # 取消编辑，不保存
                    self.editing = False
                    self.selected_setting = None
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    # 删除最后一个字符
                    self.input_text = self.input_text[:-1]
                else:
                    # 添加输入的字符
                    key_char = event.unicode
                    if key_char in "0123456789." and len(self.input_text) < 5:
                        # 确保只有一个小数点
                        if key_char == "." and "." in self.input_text:
                            return
                        self.input_text += key_char
    
    def save_setting(self):
        """保存当前设置"""
        if self.editing and self.input_text:
            try:
                value = float(self.input_text)
                # 确保速度值在0-速度上限范围内
                # 使用Settings类中定义的最大速度值
                if self.selected_setting == "ship_speed":
                    max_speed = self.ai_settings.ship_speed_max
                    min_speed = 0
                elif self.selected_setting == "alien_speed":
                    max_speed = self.ai_settings.alien_speed_max
                    min_speed = 0
                elif self.selected_setting == "bullet_speed":
                    max_speed = self.ai_settings.bullet_speed_max
                    min_speed = 0
                else:
                    max_speed = 15
                    min_speed = 0
                
                value = max(min_speed, min(max_speed, value))
                # 四舍五入保留一位小数
                value = round(value, 1)
                
                if self.selected_setting == "ship_speed":
                    self.ai_settings.ship_speed_factor = value
                elif self.selected_setting == "alien_speed":
                    self.ai_settings.alien_speed_factor = value
                elif self.selected_setting == "bullet_speed":
                    self.ai_settings.bullet_speed_factor = value
                
                # 更新显示
                self.update_buttons()
                self.editing = False
                self.selected_setting = None
                self.input_text = ""
            except ValueError:
                # 输入不是有效的数字，忽略
                self.editing = False
                self.selected_setting = None
                self.input_text = ""
    
    def update_countdown(self):
        """更新倒计时"""
        if self.countdown_active:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.countdown_start_time) // 1000
            remaining_time = self.countdown_time - elapsed_time
            
            if remaining_time <= 0:
                # 倒计时结束，恢复游戏
                self.game_paused = False
                self.countdown_active = False
                return True
            
            return remaining_time
        
        return None
    
    def draw_countdown(self):
        """绘制倒计时"""
        remaining_time = self.update_countdown()
        if remaining_time and remaining_time > 0:
            font = pygame.font.SysFont(None, 100)
            countdown_text = font.render(str(remaining_time), True, (255, 0, 0))
            countdown_rect = countdown_text.get_rect()
            countdown_rect.center = self.screen_rect.center
            self.screen.blit(countdown_text, countdown_rect)
    
    def toggle_pause(self):
        """切换游戏暂停状态"""
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.show_settings = False
            self.countdown_active = False  # 重置倒计时状态
    
    def draw(self):
        """绘制菜单"""
        if self.game_paused and not self.countdown_active:
            self.draw_menu()
        elif self.countdown_active:
            self.draw_countdown()