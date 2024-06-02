import pygame
from setting import *
from game import Game

pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('shooting game')

#FPSの設定
FPS = 60
clock = pygame.time.Clock()

#色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255 ,0)
BLUE = (0, 0, 255)

#ゲーム
game = Game()

#====================================メインループ===================================================================
run = True
while run:

    #背景の塗りつぶし
    screen.fill(BLACK)

    #ゲームの実行
    game.run()

    #イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #escapeを押したときのキーイベント    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    #更新
    pygame.display.update()
    clock.tick(FPS)


#==================================================================================================
pygame.quit()

