# enemy.py
import pygame
from setting import *
import random
from explosion import Explosion
from enemy_bullet import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, enemy_bullet_group, game):
        super().__init__(groups)
        
        self.screen = pygame.display.get_surface()
        
        # グループ
        self.enemy_bullet_group = enemy_bullet_group
        self.explosion_group = pygame.sprite.Group()
        self.game = game
        
        # 画像
        self.image_list = []
        for i in range(5):
            image = pygame.image.load(f'assets/img/enemy/{i}.png')
            self.image_list.append(image)
        
        self.index = 0
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.pre_image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        
        # 移動
        move_list = [1, -1]
        self.direction = pygame.math.Vector2((random.choice(move_list), 1))
        self.speed = 1
        self.timer = 0
        
        # 体力
        self.health = 2
        self.alive = True
        
        # 爆発
        self.explosion = False
        
        # 効果音
        self.explosion_sound = pygame.mixer.Sound('assets/sound/explosion.mp3')
        self.explosion_sound.set_volume(0.2)
        
        # 弾発射タイマー
        self.shoot_timer = 0

        # スコア値
        self.score_value = 100  # 撃破時に加算するスコア値
    
    def move(self):
        self.timer += 1
        if self.timer > 80:
            self.direction.x *= -1
            self.timer = 0
    
    def shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer > 40:  # 50フレームごとに弾を発射
            bullet = EnemyBullet(self.enemy_bullet_group, self.rect.centerx, self.rect.bottom)
            self.shoot_timer = 0
    
    def check_off_screen(self):
        if self.rect.top > screen_height:
            self.kill()
    
    def collision_bullet(self):
        # プレイヤーの弾との衝突をチェックし、敵の体力を減らす
        for bullet in self.game.player.bullet_group:
            if self.rect.colliderect(bullet.rect):
                bullet.kill()
                self.health -= 1
        
        if self.health <= 0:
            self.alive = False
    
    def check_death(self):
        if not self.alive and not self.explosion:
            explosion = Explosion(self.explosion_group, self.rect.centerx, self.rect.centery)
            self.explosion = True
            self.explosion_sound.play()
            self.game.score += self.score_value
        if self.explosion and len(self.explosion_group) == 0:
            self.kill()
        
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
    
    def animation(self):
        if self.alive:
            self.index += 0.15
            if self.index > len(self.image_list):
                self.index = 0
            
            self.pre_image = self.image_list[int(self.index)]
            self.image = pygame.transform.scale(self.pre_image, (50, 50))
        else:
            self.image.set_alpha(0)
    
    def update(self):# スプライトの状態を更新するメソッド
        self.move()# 移動メソッドを呼び出す
        self.shoot()
        self.check_off_screen()# 画面外チェックを行う
        self.animation() # アニメーションを更新する
        self.collision_bullet()# 弾との衝突をチェックする
        self.check_death()# 死亡をチェックする
        
        self.explosion_group.draw(self.screen)# 爆発グループを画面に描画する
        self.explosion_group.update() # 爆発グループを更新する
