class Settings():
    def __init__(self):
        self.screen_width = 1960
        self.screen_height = 1080
        self.bg_color = (255, 255, 204)
        # 初始速度设置
        self.ship_speed_factor = 0.4
        self.ship_limit = 3
        self.bullet_speed_factor = 1
        self.bullet_width = 3 
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.alien_speed_factor = 0.1 
        self.fleet_drop_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  
        self.alien_points = 10
        
        # 速度上限设置
        self.ship_speed_max = 10
        self.alien_speed_max = 10
        self.bullet_speed_max = 30
         