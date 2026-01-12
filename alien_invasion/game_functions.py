import sys
import random
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_events(ai_settings,screen,ship,bullets, menu, stats, pause_button, play_button=None, restart_button=None, quit_button=None, game_elements=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
           check_keydown_events(event,ai_settings,screen,ship,bullets, menu, stats)
        elif event.type == pygame.KEYUP:
           check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_mouse_events(mouse_pos, menu, pause_button, stats, play_button, restart_button, quit_button, ai_settings, screen, game_elements)
        
        # 传递所有事件给菜单处理，包括键盘输入
        menu.handle_keyboard_input(event)
            
def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button, sb, pause_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet() 
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    
    # 绘制暂停按钮
    pause_button.draw_button()
    
    # 在暂停按钮下方显示飞船生命数量
    # 使用系统中文黑体字体，支持中文显示
    font = pygame.font.SysFont("SimHei", 36)
    lives_text = font.render(f"生命：{stats.ships_left}", True, (255, 0, 0))  # 红色文字，添加中文冒号
    lives_rect = lives_text.get_rect()
    lives_rect.left = pause_button.rect.left
    lives_rect.top = pause_button.rect.bottom + 10
    screen.blit(lives_text, lives_rect)
    
    # 在游戏非活动状态时绘制Play按钮
    if not stats.game_active and not stats.game_over:
        play_button.draw_button()
    pygame.display.flip()       
    
def check_keydown_events(event,ai_settings,screen,ship,bullets, menu, stats):
    if event.key == pygame.K_RIGHT:
        ship.moving_right =True
    elif event.key == pygame.K_LEFT:
        ship.moving_left =True                
    elif event.key == pygame.K_UP:
        ship.moving_up =True                
    elif event.key == pygame.K_DOWN:
        ship.moving_down =True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        menu.toggle_pause()

def check_keyup_events(event,ship):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        if event.key == pygame.K_LEFT:
            ship.moving_left = False                
        if event.key == pygame.K_UP:
            ship.moving_up = False                
        if event.key ==pygame.K_DOWN:
            ship.moving_down = False 

def check_mouse_events(mouse_pos, menu, pause_button, stats, play_button=None, restart_button=None, quit_button=None, ai_settings=None, screen=None, game_elements=None):
    """处理鼠标点击事件"""
    # 检查是否处于游戏结束状态
    if stats.game_over:
        # 检查重新开始按钮点击
        if restart_button and restart_button.rect.collidepoint(mouse_pos):
            # 重置游戏状态
            stats.reset_stats()
            stats.game_active = True
            
            # 确保有游戏元素可以重置
            if game_elements:
                ship = game_elements['ship']
                aliens = game_elements['aliens']
                bullets = game_elements['bullets']
                sb = game_elements['sb']
                
                # 清空外星人、子弹
                aliens.empty()
                bullets.empty()
                
                # 重新创建外星人群
                creat_fleet(ai_settings, screen, ship, aliens)
                
                # 重置飞船位置
                ship.center_ship()
                
                # 重置计分板
                sb.prep_score()
        # 检查退出按钮点击
        elif quit_button and quit_button.rect.collidepoint(mouse_pos):
            sys.exit()
    # 检查是否处于游戏非活动状态（需要点击Play按钮）
    elif not stats.game_active:
        # 检查是否点击了Play按钮
        if play_button and play_button.rect.collidepoint(mouse_pos):
            # 开始游戏
            stats.reset_stats()
            stats.game_active = True
            
            # 确保有游戏元素可以重置
            if game_elements:
                ship = game_elements['ship']
                aliens = game_elements['aliens']
                bullets = game_elements['bullets']
                sb = game_elements['sb']
                
                # 清空外星人、子弹
                aliens.empty()
                bullets.empty()
                
                # 重新创建外星人群
                creat_fleet(ai_settings, screen, ship, aliens)
                
                # 重置飞船位置
                ship.center_ship()
                
                # 重置计分板
                sb.prep_score()
    else:
        # 检查是否点击了暂停按钮
        if pause_button.rect.collidepoint(mouse_pos):
            menu.toggle_pause()
        else:
            # 检查菜单按钮点击
            result = menu.check_button_click(mouse_pos)
            if result == "quit":
                sys.exit()

def update_bullets(ai_settings,screen,ship, aliens, bullets, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,ship, aliens, bullets, stats, sb)

def check_bullet_alien_collisions(ai_settings,screen,ship, aliens, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True, True) 
    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)
        sb.prep_score()
    # 当外星人数量不足时，随机补充1-2个外星人
    while len(aliens) < 1:
        alien = Alien(ai_settings, screen)
        aliens.add(alien)

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width-2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x    

def get_number_rows(ai_settings,ship_height, alien_height):
    available_space_y = (ai_settings.screen_height-(3*alien_height)- ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def creat_fleet(ai_settings,screen,ship,aliens):
    # 随机生成1-6个外星人
    alien_count = random.randint(1, 6)
    for _ in range(alien_count):
        alien = Alien(ai_settings, screen)
        aliens.add(alien)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed 
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,stats,screen, ship, aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    # 将ship传递给alien.update()，使外星人追踪飞船
    aliens.update(ship)
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats,screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings,stats,screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats,screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -=1
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings,screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        stats.game_over = True

def check_aliens_bottom(ai_settings,stats,screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.copy():
        if alien.rect.bottom >= screen_rect.bottom:
            aliens.remove(alien)  # 外星人到达底部后直接消失，不影响飞船生命


