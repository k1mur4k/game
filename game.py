import pygame  
from setting import *  
from player import Player  
from enemy import Enemy  
import random  
from support import draw_text  

class Game:

    def __init__(self):
        self.screen = pygame.display.get_surface()  # ゲームのメインスクリーンを取得

        # グループの作成
        self.create_group()

        # 自機
        self.player = Player(self.player_group, 300, 500, self.enemy_group)  # プレイヤーを初期位置に配置

        # 敵
        self.timer = 0  # 敵生成のタイマー

        # 背景
        self.pre_bg_img = pygame.image.load('assets/img/background/bg.png')  # 背景画像をロード
        self.bg_img = pygame.transform.scale(self.pre_bg_img, (screen_width, screen_height))  # 画面サイズに合わせてスケール
        self.bg_y = 0  # 背景のy座標
        self.scroll_speed = 0.5  # 背景スクロールの速度

        # ゲームオーバー
        self.game_over = False  # ゲームオーバーフラグ

        # BGM（いいBGMがあれば）
        # pygame.mixer.music.load('assets/sound/bgm.mp3')
        # pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.3)

        # スコア
        self.score = 0  # スコアを管理する変数を追加

    def create_group(self):
        self.player_group = pygame.sprite.GroupSingle()  # プレイヤー用のグループ
        self.enemy_group = pygame.sprite.Group()  # 敵用のグループ

    def create_enemy(self):
        self.timer += 1  # タイマーをインクリメント
        if self.timer > 30:  # 50フレームごとに
            enemy = Enemy(self.enemy_group, random.randint(50, 550), 0, self.player.bullet_group,self)  # ランダムな位置に敵を生成
            self.timer = 0  # タイマーをリセット

    def player_death(self):
        if len(self.player_group) == 0:  # プレイヤーグループが空の場合
            self.game_over = True  # ゲームオーバーフラグをTrueに設定
            draw_text(self.screen, 'game over', screen_width // 2, screen_height //2, 75, RED)  # ゲームオーバーテキストを表示
            draw_text(self.screen, 'press SPACE KEY to reset', screen_width//2, screen_height//2 + 100, 50, RED)  # リセット指示テキストを表示

    def reset(self):
        key = pygame.key.get_pressed()  # キーボードの状態を取得
        if self.game_over and key[pygame.K_SPACE]:  # ゲームオーバー状態でスペースキーが押された場合
            self.player = Player(self.player_group, 300, 500, self.enemy_group)  # プレイヤーを再生成
            self.enemy_group.empty()  # 敵グループを空にする
            self.game_over = False  # ゲームオーバーフラグをFalseに設定
            self.score = 0  # スコアをリセット

    # 画像のスクロール
    def scroll_bg(self):
        # ここで速度を変更できる
        self.bg_y = (self.bg_y + self.scroll_speed) % screen_height  # 背景をスクロール
        self.screen.blit(self.bg_img, (0, self.bg_y - screen_height))  # 背景を描画（ラップアラウンド）
        self.screen.blit(self.bg_img, (0, self.bg_y))  # 背景を描画

    def run(self):
        self.scroll_bg()  # 背景をスクロール

        self.create_enemy()  # 敵を生成

        self.player_death()  # プレイヤーの死亡チェック
        self.reset()  # ゲームのリセット

        # グループの描画と更新
        self.player_group.draw(self.screen)  # プレイヤーグループを描画
        self.player_group.update()  # プレイヤーグループを更新
        self.enemy_group.draw(self.screen)  # 敵グループを描画
        self.enemy_group.update()  # 敵グループを更新

        # スコアの表示
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # print(self.enemy_group)  # 敵グループのデバッグ出力（コメントアウト）
