import pygame  
from setting import *  

class Explosion(pygame.sprite.Sprite):  # Explosionクラスを定義し、pygameのSpriteクラスから継承する
    def __init__(self, groups, x, y):  # イニシャライザ（コンストラクタ）。グループ、x座標、y座標を引数に取る
        super().__init__(groups)  # pygameのSpriteクラスのコンストラクタを呼び出し、グループを引数にする

        # 画像
        self.image_list = []  # 画像を格納するリストを初期化
        for i in range(5):  # 5回繰り返す
            image = pygame.image.load(f'assets/img/explosion/{i}.png')  # 画像をロードし、imageに格納
            self.image_list.append(image)  # ロードした画像をimage_listに追加

        self.index = 0  # 現在の画像のインデックスを0に初期化
        self.pre_image = self.image_list[self.index]  # 現在のインデックスの画像をpre_imageに格納
        self.image = pygame.transform.scale(self.pre_image, (50,50))  # pre_imageを50x50にスケールし、imageに格納
        self.rect = self.image.get_rect(center = (x,y))  # imageの矩形を取得し、中心を(x, y)に設定

    def animation(self):  # アニメーションを処理するメソッド
        self.index += 0.2  # インデックスを0.2増加させる

        if self.index < len(self.image_list):  # インデックスが画像リストの長さ未満の場合
            self.pre_image = self.image_list[int(self.index)]  # インデックスに対応する画像をpre_imageに更新
            self.image = pygame.transform.scale(self.pre_image, (50,50))  # pre_imageを50x50にスケールし、imageに更新
        else:  # インデックスが画像リストの長さ以上の場合
            self.kill()  # スプライトを全てのグループから削除

    def update(self):  # スプライトの状態を更新するメソッド
        self.animation()  # アニメーションメソッドを呼び出す
