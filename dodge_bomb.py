import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外か判定
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横, 縦）/ 画面内True, 画面外False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に画面に「Game Over」を表示し、泣いているこうかとんを描画する。
    引数：screen - 描画するスクリーンSurface
    """
    # 半透明の黒い背景
    overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # "Game Over" テキストの描画
    font = pg.font.Font(None, 120)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, text_rect)
    
    # 泣いているこうかとんを描画
    kk_cry_img = pg.transform.rotozoom(pg.image.load("fig/9.png"), 0, 0.9)  # 泣いているこうかとん画像
    kk_cry_left_rect = kk_cry_img.get_rect(midright=(text_rect.left - 20, text_rect.centery)) #左側のこうかとん
    screen.blit(kk_cry_img,kk_cry_left_rect)
    kk_cry_right_rect = kk_cry_img.get_rect(midleft=(text_rect.right + 20, text_rect.centery)) #右側のこうかとん
    screen.blit(kk_cry_img,kk_cry_right_rect)

    
    pg.display.update()
    pg.time.wait(5000)  # 5秒間停止


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す。
    """
    bb_imgs = [pg.Surface((size, size), pg.SRCALPHA) for size in range(10, 110, 10)]
    for i, img in enumerate(bb_imgs):
        pg.draw.circle(img, (255, 0, 0), (img.get_width() // 2, img.get_height() // 2), img.get_width() // 2)
    bb_accs = [i for i in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル

    clock = pg.time.Clock()
    tmr = 0
    muki = 0
    sayu = False
    



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            game_over(screen)  # ゲームオーバー画面を表示
            return

        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:

                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
                if tpl == (0, -5):  # 上
                    muki = 0
                elif tpl == (-5,-5):  #左上
                    muki = -45
                elif tpl == (0, 5):  # 下
                    muki = 180
                elif tpl == (-5,5):
                    muki = -225
                elif tpl == (-5,0):  #左
                    muki = 0
                elif tpl == (5, 0):  # 右
                    muki = -180
    
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        rotated_kk_img = pg.transform.rotate(kk_img,muki)
        rotated_kk_rct = rotated_kk_img.get_rect(center=kk_rct.center)
        screen.blit(rotated_kk_img, rotated_kk_rct)

        # 爆弾の移動処理
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        # 爆弾のサイズと速度の上昇
        bb_img = bb_imgs[min(tmr // 500, 9)]  # サイズは最大で9番目まで
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        vx = bb_accs[min(tmr // 500, 9)] * (1 if vx > 0 else -1)
        vy = bb_accs[min(tmr // 500, 9)] * (1 if vy > 0 else -1)

        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
