import pygame  
from setting import *  
import random  
from explosion import Explosion  

class Enemy(pygame.sprite.Sprite):  # Enemyクラスを定義し、pygameのSpriteクラスから継承
    def __init__(self, groups, x, y, bullet_group, game):  # 初期化メソッド。グループ、x座標、y座標、弾のグループを引数に取る
        super().__init__(groups)  # pygameのSpriteクラスの初期化メソッドを呼び出す

        self.screen = pygame.display.get_surface()  # ゲームのメインスクリーンを取得

        # グループ
        self.bullet_group = bullet_group  # 弾のグループを保存
        self.explosion_group = pygame.sprite.Group()  # 爆発のためのスプライトグループを作成
        self.game = game  # Gameクラスのインスタンスを保持

        # 画像
        self.image_list = []  # 画像リストを初期化
        for i in range(5):  # 5枚の画像を読み込む
            image = pygame.image.load(f'assets/img/enemy/{i}.png')  # 画像をロード
            self.image_list.append(image)  # リストに画像を追加

        self.index = 0  # 画像リストの現在のインデックス
        self.pre_image = self.image_list[self.index]  # 現在の画像
        self.image = pygame.transform.scale(self.pre_image, (50, 50))  # 画像を50x50にスケーリング
        self.rect = self.image.get_rect(center=(x, y))  # 画像の矩形を取得し、中心を(x, y)に設定

        # 移動
        move_list = [1, -1]  # 左または右に動くためのリスト
        self.direction = pygame.math.Vector2((random.choice(move_list), 1))  # 移動方向をランダムに選択
        self.speed = 1  # 移動速度
        self.timer = 0  # 方向転換のためのタイマー

        # 体力
        self.health = 3  # 敵の体力
        self.alive = True  # 敵が生きているかのフラグ

        # 爆発
        self.explosion = False  # 爆発が発生したかのフラグ

        # 効果音
        self.explosion_sound = pygame.mixer.Sound('assets/sound/explosion.mp3')  # 爆発音をロード
        self.explosion_sound.set_volume(0.2)  # 音量を設定

        # スコア値
        self.score_value = 100  # 撃破時に加算するスコア値

    def move(self):  # 敵の移動を制御するメソッド
        self.timer += 1  # タイマーを増加

        if self.timer > 80:  # タイマーが80を超えたら
            self.direction.x *= -1  # 移動方向を反転
            self.timer = 0  # タイマーをリセット

    def check_off_screen(self):  # 画面外に出たかチェックするメソッド
        if self.rect.top > screen_height:  # 画面の上端を超えたら
            self.kill()  # スプライトを削除

    def collision_bullet(self):  # 弾との衝突をチェックするメソッド
        for bullet in self.bullet_group:  # 全ての弾に対して
            if self.rect.colliderect(bullet.rect):  # 弾と衝突した場合
                bullet.kill()  # 弾を削除
                self.health -= 1  # 体力を減らす

        if self.health <= 0:  # 体力が0以下になったら
            self.alive = False  # 敵を死亡状態にする
    
    def check_death(self):  # 敵の死亡を処理するメソッド
        if not self.alive and not self.explosion:  # 敵が死亡し、まだ爆発していない場合
            explosion = Explosion(self.explosion_group, self.rect.centerx, self.rect.centery)  # 爆発を生成
            self.explosion = True  # 爆発フラグを真にする
            self.explosion_sound.play()  # 爆発音を再生
            self.game.score += self.score_value  # 敵を撃破したときにスコアを加算
        if self.explosion and len(self.explosion_group) == 0:  # 爆発が終了した場合
            self.kill()  # 敵を削除

        # 移動
        self.rect.x += self.direction.x * self.speed  # x方向に移動
        self.rect.y += self.direction.y * self.speed  # y方向に移動

    def animation(self):  # アニメーションを更新するメソッド
        if self.alive:  # 生きている場合
            self.index += 0.15  # インデックスを増加
            if self.index > len(self.image_list):  # インデックスが画像リストを超えた場合
                self.index = 0  # インデックスをリセット

            self.pre_image = self.image_list[int(self.index)]  # 現在の画像を更新
            self.image = pygame.transform.scale(self.pre_image, (50, 50))  # 画像をスケーリング
        else:  # 死亡している場合
            self.image.set_alpha(0)  # 画像を透明にする

    def update(self):  # スプライトの状態を更新するメソッド
        self.move()  # 移動メソッドを呼び出す
        self.check_off_screen()  # 画面外チェックを行う
        self.animation()  # アニメーションを更新する
        self.collision_bullet()  # 弾との衝突をチェックする
        self.check_death()  # 死亡をチェックする

        # グループの描画と更新
        self.explosion_group.draw(self.screen)  # 爆発グループを画面に描画する
        self.explosion_group.update()  # 爆発グループを更新する
