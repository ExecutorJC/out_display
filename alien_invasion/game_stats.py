class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # 初始游戏状态为非活动，需要点击Play按钮才开始
        self.game_active = False
        self.game_over = False
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.game_over = False