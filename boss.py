# boss.py
import pygame
from setting import *
from enemy_bullet import EnemyBullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, bullet_group, game):
        super().__init__(groups)
        
        self.screen = pygame.display.get_surface()
        
        # グループ
        self.bullet_group = bullet_group
        self.game = game
        
        # 画像
        self.image = pygame.image.load('assets/img/enemy/boss.png')
        self.image = pygame.transform.scale(self.image, (100, 120))
        self.rect = self.image.get_rect(center=(x, y))
        
        # 移動
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 2
        self.timer = 0
        
        # 体力
        self.health = 30
        self.alive = True
        
        # 弾発射タイマー
        self.shoot_timer = 0
    
    def move(self):
        self.rect.x += self.direction.x * self.speed
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction.x *= -1
    
    def shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer > 30:  # 20フレームごとに弾を発射
            self.shoot_timer = 0
            # 中央の弾
            bullet = EnemyBullet(self.bullet_group, self.rect.centerx, self.rect.bottom)
            # 左側の斜め弾
            left_bullet = EnemyBullet(self.bullet_group, self.rect.centerx - 20, self.rect.bottom)
            left_bullet.direction = pygame.math.Vector2(-0.5, 1)
            # 右側の斜め弾
            right_bullet = EnemyBullet(self.bullet_group, self.rect.centerx + 20, self.rect.bottom)
            right_bullet.direction = pygame.math.Vector2(0.5, 1)
            # グループに追加
            self.bullet_group.add(bullet, left_bullet, right_bullet)
    
    def check_off_screen(self):
        if self.rect.top > screen_height:
            self.kill()
    
    def collision_bullet(self):
        # プレイヤーの弾との衝突をチェックし、ボスの体力を減らす
        for bullet in self.game.player.bullet_group:
            if self.rect.colliderect(bullet.rect):
                bullet.kill()
                self.health -= 1
        
        if self.health <= 0:
            self.alive = False
    
    def check_death(self):
        if not self.alive:
            self.kill()
            self.game.game_clear = True  # ゲームクリアに設定
    
    def update(self):
        self.move()
        self.shoot()
        self.check_off_screen()
        self.collision_bullet()
        self.check_death()
