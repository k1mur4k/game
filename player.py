import pygame  
from setting import *  
from bullet import Bullet  

class Player(pygame.sprite.Sprite):  # Playerクラスを定義し、pygameのSpriteクラスから継承

    def __init__(self, groups, x, y, enemy_group):  # 初期化メソッド。グループ、x座標、y座標、敵のグループを引数に取る
        super().__init__(groups)  # pygameのSpriteクラスの初期化メソッドを呼び出す

        self.screen = pygame.display.get_surface()  # ゲームのメインスクリーンを取得

        # グループ
        self.bullet_group = pygame.sprite.Group()  # 弾のためのスプライトグループを作成
        self.enemy_group = enemy_group  # 敵のグループを保存

        # 画像
        self.image_list = []  # 画像リストを初期化
        for i in range(3):  # 3枚の画像を読み込む
            image = pygame.image.load(f'assets/img/player/{i}.png')  # 画像をロード
            self.image_list.append(image)  # リストに画像を追加

        self.index = 0 # 初期状態の画像インデックス
        self.pre_image = self.image_list[self.index]  # 現在の画像
        self.image = pygame.transform.scale(self.pre_image, (50, 50))  # 画像を50x50にスケーリング
        self.rect = self.image.get_rect(center=(x, y))  # 画像の矩形を取得し、中心を(x, y)に設定

        # 移動
        self.direction = pygame.math.Vector2()  # 移動方向ベクトルを初期化
        self.speed = 5  # 移動速度

        # 弾
        self.fire = False  # 弾を発射中かどうかのフラグ
        self.timer = 0  # 弾発射のクールダウンタイマー

        # 体力
        self.health = 1  # プレイヤーの体力
        self.alive = True  # プレイヤーが生きているかのフラグ

        # 効果音
        self.shot_sound = pygame.mixer.Sound('assets/sound/shot.mp3')  # 発射音をロード
        self.shot_sound.set_volume(0.2)  # 音量を設定

    def input(self):  # プレイヤーの入力を処理するメソッド
        key = pygame.key.get_pressed()  # キーボードの状態を取得

        # ボタン操作
        if key[pygame.K_UP]:  # 上キーが押されている場合
            self.direction.y = -1
        elif key[pygame.K_DOWN]:  # 下キーが押されている場合
            self.direction.y = 1
        else:  # 上下キーが押されていない場合
            self.direction.y = 0

        if key[pygame.K_LEFT]:  # 左キーが押されている場合
            self.direction.x = -1
            self.index = 1  # 左向きの画像
        elif key[pygame.K_RIGHT]:  # 右キーが押されている場合
            self.direction.x = 1
            self.index = 2  # 右向きの画像
        else:  # 左右キーが押されていない場合
            self.direction.x = 0
            self.index = 0  # 前向きの画像

        if key[pygame.K_z] and not self.fire:  # Zキーが押され、かつ発射フラグがFalseの場合
            bullet = Bullet(self.bullet_group, self.rect.centerx, self.rect.top)  # 弾を生成
            self.fire = True  # 発射フラグをTrueに設定
            self.shot_sound.play()  # 発射音を再生

    def cooldown_bullet(self):  # 弾のクールダウンを処理するメソッド
        if self.fire:  # 発射フラグがTrueの場合
            self.timer += 1  # タイマーを増加
        if self.timer > 10:  # タイマーが10を超えた場合
            self.fire = False  # 発射フラグをFalseに設定
            self.timer = 0  # タイマーをリセット
    
    def move(self):  # プレイヤーの移動を処理するメソッド
        if self.direction.magnitude() != 0:  # 移動方向ベクトルの大きさが0でない場合
            self.direction.normalize()  # 方向ベクトルを正規化

        self.rect.x += self.direction.x * self.speed  # x方向に移動
        self.check_off_screen('horizontal')  # 水平方向の画面外チェック
        self.rect.y += self.direction.y * self.speed  # y方向に移動
        self.check_off_screen('vertical')  # 垂直方向の画面外チェック

    def check_off_screen(self, direction):  # 画面外に出たかチェックするメソッド
        if direction == 'horizontal':  # 水平方向のチェックの場合
            if self.rect.left < 0:  # 左端が画面外に出た場合
                self.rect.left = 0
            if self.rect.right > screen_width:  # 右端が画面外に出た場合
                self.rect.right = screen_width

        if direction == 'vertical':  # 垂直方向のチェックの場合
            if self.rect.top < 0:  # 上端が画面外に出た場合
                self.rect.top = 0
            if self.rect.bottom > screen_width:  # 下端が画面外に出た場合
                self.rect.bottom = screen_height
    
    def collision_enemy(self):  # 敵との衝突をチェックするメソッド
        for enemy in self.enemy_group:  # 全ての敵に対して
            if self.rect.colliderect(enemy.rect) and enemy.alive:  # 敵と衝突し、かつ敵が生きている場合
                self.health -= 1  # 体力を減らす

        if self.health <= 0:  # 体力が0以下になった場合
            self.alive = False  # 生存フラグをFalseに設定

    def check_death(self):  # 死亡チェックを行うメソッド
        if not self.alive:  # 生存フラグがFalseの場合
            self.kill()  # スプライトを削除する

    def update_image(self):  # 画像を更新するメソッド
        self.pre_image = self.image_list[self.index]  # 現在の画像インデックスに基づいて画像を更新
        self.image = pygame.transform.scale(self.pre_image, (50, 50))  # 画像をスケーリング

    def update(self):  # スプライトの状態を更新するメソッド
        self.input()  # 入力を処理
        self.move()  # 移動を処理
        self.update_image()  # 画像を更新
        self.cooldown_bullet()  # 弾のクールダウンを処理
        self.collision_enemy()  # 敵との衝突をチェック
        self.check_death()  # 死亡をチェック

        # グループの描画と更新
        self.bullet_group.draw(self.screen)  # 弾のグループを画面に描画
        self.bullet_group.update()  # 弾のグループを更新
        # テスト用
        # print(self.bullet_group)
