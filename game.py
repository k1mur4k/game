import pygame
import time  # timeモジュールをインポート
from setting import *
from player import Player
from enemy import Enemy
from boss import Boss  # Bossクラスをインポート
import random
from support import draw_text

class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.create_group()
        self.player = Player(self.player_group, 300, 500, self.enemy_group)
        self.timer = 0
        
        # BGM（特にいいBGMがありませんでした）
        pygame.mixer.music.load('assets/sound/bgm.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        
        # 背景
        self.pre_bg_img = pygame.image.load('assets/img/background/bg.png')
        self.bg_img = pygame.transform.scale(self.pre_bg_img, (screen_width, screen_height))
        self.bg_y = 0
        self.scroll_speed = 0.5
        
        # ゲームオーバーとゲームクリア
        self.game_over = False
        self.game_clear = False
        
        # スコア
        self.score = 0
        
        # ゲーム開始時間
        self.start_time = time.time()
        self.end_time = None  # ゲーム終了時間
        self.clear_time = None  # ゲームクリア時間
        
        # ボスフラグ
        self.boss_spawned = False
    
    def create_group(self):
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()  # ボスグループを追加
    
    def create_enemy(self):
        self.timer += 1
        if self.timer > 50:
            enemy = Enemy(self.enemy_group, random.randint(50, 550), 0, self.enemy_bullet_group, self)
            self.timer = 0
    
    def create_boss(self):
        boss = Boss(self.boss_group, screen_width // 2, 100, self.enemy_bullet_group, self)
        self.boss_spawned = True
    
    def player_death(self):
        if not self.game_over:  # 初回のみゲームオーバー時間を記録
            self.end_time = time.time()
            self.game_over = True
        draw_text(self.screen, 'YOU DIED', screen_width // 2, screen_height // 2, 75, RED)
        draw_text(self.screen, 'Press SPACE KEY to reset', screen_width // 2, screen_height // 2 + 100, 50, RED)
        elapsed_time = self.end_time - self.start_time
        draw_text(self.screen, f'Time: {elapsed_time:.2f} seconds', screen_width // 2, screen_height // 2 + 150, 50, WHITE)
    
    def reset(self):
        key = pygame.key.get_pressed()
        if (self.game_over or self.game_clear) and key[pygame.K_SPACE]:
            self.player = Player(self.player_group, 300, 500, self.enemy_group)
            self.enemy_group.empty()
            self.enemy_bullet_group.empty()
            self.boss_group.empty()  # ボスグループをクリア
            self.game_over = False
            self.game_clear = False
            self.start_time = time.time()  # ゲーム開始時間をリセット
            self.end_time = None  # ゲーム終了時間をリセット
            self.clear_time = None  # ゲームクリア時間をリセット
            self.boss_spawned = False
            self.score = 0  # スコアをリセット
    
    def scroll_bg(self):
        self.bg_y = (self.bg_y + self.scroll_speed) % screen_height
        self.screen.blit(self.bg_img, (0, self.bg_y - screen_height))
        self.screen.blit(self.bg_img, (0, self.bg_y))
    
    def run(self):
        self.scroll_bg()
        if not self.game_over and not self.game_clear:
            if not self.boss_spawned and self.score >= 1000:  # スコアが1000に達したらボスを生成
                self.create_boss()
            if not self.boss_spawned:
                self.create_enemy()
            
            self.player_group.update()
            self.enemy_group.update()
            self.enemy_bullet_group.update()
            self.boss_group.update()
            
            # プレイヤーが敵の弾に当たったかどうかをチェック
            for bullet in self.enemy_bullet_group:
                if self.player.rect.colliderect(bullet.rect):
                    bullet.kill()
                    self.player.health -= 1
                    if self.player.health <= 0:
                        self.player_death()
        
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.enemy_bullet_group.draw(self.screen)
        self.boss_group.draw(self.screen)  # ボスグループを描画

        if self.game_clear:
            if self.clear_time is None:
                self.clear_time = time.time() - self.start_time  # ゲームクリア時の経過時間を記録
            draw_text(self.screen, 'GAME CLEAR', screen_width // 2, screen_height // 2, 75, GREEN)
            draw_text(self.screen, 'Press SPACE KEY to reset', screen_width // 2, screen_height // 2 + 100, 50, GREEN)
            draw_text(self.screen, f'Time: {self.clear_time:.2f} seconds', screen_width // 2, screen_height // 2 + 150, 50, WHITE)

        if self.game_over:
            self.player_death()

        self.reset()
