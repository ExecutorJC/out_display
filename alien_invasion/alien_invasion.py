import sys
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from scoreboard import Scoreboard
from menu import Menu

def run_game():
    pygame.init()
    ai_settings = Settings()    
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    # 创建暂停按钮，放置在屏幕左上角
    pause_button = Button(ai_settings, screen, "暂停", position=(10, 10))
    # 创建游戏结束按钮
    restart_button = Button(ai_settings, screen, "重新开始")
    quit_button = Button(ai_settings, screen, "退出")
    stats = GameStats(ai_settings) 
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    menu = Menu(ai_settings, screen)
    gf.creat_fleet(ai_settings,screen,ship,aliens)

    # 添加暂停画面保存变量
    paused_screen = None
    
    while True:
        # 检查事件，包括菜单事件
        # 保存当前的游戏元素引用，以便在重新开始时使用
        game_elements = {
            'ship': ship,
            'aliens': aliens,
            'bullets': bullets,
            'sb': sb
        }
        
        # 检查事件，传递游戏元素以便重新开始时使用
        gf.check_events(ai_settings, screen, ship, bullets, menu, stats, pause_button, play_button, restart_button, quit_button, game_elements)
        
        # 如果游戏未暂停且处于活动状态，更新游戏状态
        if stats.game_active and not menu.game_paused:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets, stats, sb)  
            gf.update_aliens(ai_settings,stats,screen, ship, aliens,bullets)  
            # 正常绘制游戏界面
            gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button, sb, pause_button)
            # 清除暂停画面，确保下次暂停时重新保存
            paused_screen = None
        
        # 检查菜单状态
        elif menu.game_paused:
            # 绘制保存的游戏画面，只在需要时保存
            if paused_screen is None:
                paused_screen = screen.copy()
            
            # 绘制保存的游戏画面
            screen.blit(paused_screen, (0, 0))
            # 绘制菜单
            menu.draw()
            # 只在暂停状态首次进入时刷新，避免频繁刷新导致闪烁
            pygame.display.flip()
        
        # 检查游戏结束状态
        elif stats.game_over:
            # 绘制游戏结束画面
            # 填充黑色背景
            screen.fill((0, 0, 0))
            
            # 使用系统中文黑体字体，支持中文显示
            font = pygame.font.SysFont("SimHei", 120)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # 红色文字
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = screen.get_rect().center
            screen.blit(game_over_text, game_over_rect)
            
            # 绘制最终得分
            sb.show_score()
            
            # 计算按钮位置，水平左右放置
            button_y = game_over_rect.bottom + 50
            button_spacing = 20  # 按钮之间的间距
            
            # 临时保存按钮的背景色，改为明显的颜色
            original_restart_bg = restart_button.button_color
            original_quit_bg = quit_button.button_color
            
            # 改为明显的背景色，确保按钮可见
            restart_button.button_color = (0, 255, 0)  # 绿色背景
            quit_button.button_color = (255, 0, 0)  # 红色背景
            
            # 重新创建按钮，确保宽度和文字正确
            restart_button = Button(ai_settings, screen, "重新开始")
            quit_button = Button(ai_settings, screen, "退出")
            
            # 获取两个按钮中较宽的宽度，确保背景框对齐
            max_button_width = max(restart_button.width, quit_button.width)
            
            # 设置两个按钮具有相同的宽度，确保背景框对齐
            restart_button.width = max_button_width
            quit_button.width = max_button_width
            
            # 计算总宽度（两个按钮宽度 + 间距）
            total_width = restart_button.width * 2 + button_spacing
            
            # 设置按钮位置，使其水平居中，左右排列
            restart_button.rect.centerx = screen.get_rect().centerx - (total_width // 2) + (restart_button.width // 2)
            restart_button.rect.y = button_y
            
            quit_button.rect.centerx = screen.get_rect().centerx + (total_width // 2) - (quit_button.width // 2)
            quit_button.rect.y = button_y
            
            # 绘制按钮，不再调用_prep_msg()，避免位置重置
            # 绘制按钮背景
            pygame.draw.rect(screen, restart_button.button_color, restart_button.rect)
            pygame.draw.rect(screen, quit_button.button_color, quit_button.rect)
            # 绘制按钮文字
            restart_msg = restart_button.font.render(restart_button.msg, True, restart_button.text_color)
            restart_msg_rect = restart_msg.get_rect()
            restart_msg_rect.center = restart_button.rect.center
            screen.blit(restart_msg, restart_msg_rect)
            
            quit_msg = quit_button.font.render(quit_button.msg, True, quit_button.text_color)
            quit_msg_rect = quit_msg.get_rect()
            quit_msg_rect.center = quit_button.rect.center
            screen.blit(quit_msg, quit_msg_rect)
            
            # 恢复原始背景色
            restart_button.button_color = original_restart_bg
            quit_button.button_color = original_quit_bg
            
            pygame.display.flip()
        
        # 初始状态：游戏未活动、未暂停、未结束
        else:
            # 绘制游戏初始画面，包括Play按钮
            gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button, sb, pause_button)
run_game()