#-*-coding:utf-8-*-
import pygame
import sys
from pygame.locals import *
import player
import bullet
import virus

#初始化pygame
pygame.init()
pygame.mixer.init()

#设置游戏屏幕大小
bg_size = width,height = 600,600
#设置游戏界面大小
screen = pygame.display.set_mode(bg_size)
#标题和背景
pygame.display.set_caption("病毒大战")
background = pygame.image.load("resources/image/bg.png").convert_alpha()

#欢迎页面背景
start_image= pygame.transform.scale(pygame.image.load("resources/image/start.png").convert_alpha(),(600, 630))
begin_image=pygame.transform.scale(pygame.image.load("resources/image/begin.png").convert_alpha(),(160, 60))
#设置游戏循环帧数
clock = pygame.time.Clock()

#音效
background_music_path = "resources/sound/background.wav"
win_music_path = "resources/sound/winmusic.wav"
gameover_music_path = "resources/sound/death.wav"
bullet_music_path="resources/sound/bullet.wav"

#读取最高得分
def record_score(score):
    # 读取历史最高得分
    with open("maxScore.txt", "r") as f:
        stream = f.read()
        if stream == '':
            stream = f.read() + '0-0'
        msg_list = str(stream).split("-")
        max_score = int(msg_list[1])
    # 如果玩家得分大于历史最高分，则存档
    if score > max_score:
        with open("maxScore.txt", "w",encoding='utf-8') as f:
            f.write(str(score))
    return str(max_score)


#病毒分组
def add_small_virus(group1,group2,n):
    for i in range(n):
        v1 = virus.Small_virus(bg_size)
        group1.add(v1)
        group2.add(v1)

def add_mid_virus(group1,group2,n):
    for i in range(n):
        v1 = virus.Mid_virus(bg_size)
        group1.add(v1)
        group2.add(v1)

def add_big_virus(group1,group2,n):
    for i in range(n):
        v1 = virus.Big_virus(bg_size)
        group1.add(v1)
        group2.add(v1)


def main():

    # 存放全部细菌
    virus_group = pygame.sprite.Group()
    # 存放三种细胞的组
    small_virus = pygame.sprite.Group()
    add_small_virus(virus_group, small_virus, 5)
    mid_virus = pygame.sprite.Group()
    add_mid_virus(virus_group, mid_virus, 10)
    big_virus = pygame.sprite.Group()
    add_big_virus(virus_group, big_virus, 5)

    # 生成玩家
    player1 = player.Player(bg_size)

    # 创建子弹组
    bullets = []
    # 子弹索引
    bullet_index = 0
    maxBullets = 6
    # 生成子弹
    for i in range(0, maxBullets):
        bullets.append(bullet.Bullet(player1.rect.midtop))

    # 通关
    success = pygame.transform.scale(pygame.image.load("resources/image/success.png").convert_alpha(), (600, 600))
    success_rect = success.get_rect()
    # gameover
    gameover = pygame.transform.scale(pygame.image.load("resources/image/lose.png").convert_alpha(), (600, 600))
    gameover_rect = gameover.get_rect()
    text_font = pygame.font.Font(None, 66)
    recorded = False
    # 游戏结束界面
    again_image = pygame.image.load("resources/image/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    return_image = pygame.image.load("resources/image/return.png").convert_alpha()
    return_rect = return_image.get_rect()
    restart_image = pygame.transform.scale(pygame.image.load("resources/image/restart.png").convert_alpha(), (112, 28))
    restart_rect = restart_image.get_rect()
    # 设定延迟
    delay = 100

    # 定义变量
    startbutton = False
    background_sound_flag = True
    win_sound_flag = True
    gameover_sound_flag = True
    active = True
    score = 0
    life = 10
    # 字体
    score_font = pygame.font.Font(None, 48)

    # 游戏主循环
    while True:
        # 绘制游戏最大帧数 60
        clock.tick(60)
        # 绘制首页
        if not startbutton:
            screen.blit(start_image, (0, 0))
            screen.blit(begin_image, (380, 460))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    # 获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    # 如果鼠标在“重新开始”上
                    print(str(pos))
                    if 380 < pos[0] < 500 and 460 < pos[1] < 520:
                        startbutton = True
        elif startbutton and player1.active and active and score < 100:
            if background_sound_flag:
                background_sound_flag = False
                win_sound_flag, gameover_sound_flag = True, True
                pygame.mixer.init()
                pygame.mixer.music.load(background_music_path)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer_music.play(-1)

            # 绘制背景
            screen.blit(background, (0, 0))

            # 绘制玩家
            screen.blit(player1.image, player1.rect)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_UP]:
                player1.moveUp()
            if key_pressed[K_DOWN]:
                player1.moveDown()
            if key_pressed[K_LEFT]:
                player1.moveLeft()
            if key_pressed[K_RIGHT]:
                player1.moveRight()

            # 检测玩家是否和病毒碰撞
            virus_down = pygame.sprite.spritecollide(player1, virus_group, False)
            if virus_down:
                player1.active = False
                for each in virus_down:
                    each.active = False

            # 装填子弹
            if delay % 15 == 0:
                bullets[bullet_index].reset(player1.rect.midtop)
                bullet_index = (bullet_index + 1) % maxBullets
            delay -= 1
            if delay == 0:
                delay = 100
            # 发射子弹
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    virus_hit = pygame.sprite.spritecollide(b, virus_group, False, pygame.sprite.collide_mask)
                    if virus_hit:
                        b.active = False
                        for e in virus_hit:
                            e.active = False

            if player1.active:
                screen.blit(player1.image, player1.rect)
            # 绘制三种细胞
            for each in small_virus:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    score += each.score
                    each.reset()
            for each in mid_virus:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    score += each.score
                    each.reset()
            for each in big_virus:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    score += each.score
                    each.reset()

            for each in virus_group:
                if each.rect.bottom > height:
                    life -= 1
                    each.active = False

            if life < 1:
                active = False

            # 绘制分数
            score_text = score_font.render("Score : {0}".format(score), True, (255, 255, 255))
            screen.blit(score_text, (0, 0), )
            # 绘制剩余生命值
            life_text = score_font.render("Life : {0}".format(life), True, (255, 255, 255))
            screen.blit(life_text, (10, height - 60))

        elif startbutton and score >= 100:
            if win_sound_flag:
                win_sound_flag = False
                gameover_sound_flag, background_sound_flag = True, True
                pygame.mixer.init()
                pygame.mixer.music.load(win_music_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)

            screen.blit(success, (0,0))

            # 判断是否将分数记录在记录文件中
            if not recorded:
                recorded = True
                record_score(score)

            # 绘制文本
            s="Winner"
            text_image = text_font.render(str(s), True, (0, 0, 0))
            text_image_rect = text_image.get_rect()
            screen.blit(text_image, ((width - text_image_rect.width) // 2, 200))

            # 绘制重新开始按钮图标
            restart_rect.left, restart_rect.top = (width - restart_rect.width) // 2, \
                                                  height // 1.5 + 20
            screen.blit(restart_image, restart_rect)
            # 绘制退出游戏按钮图标
            return_rect.left, return_rect.top = (width - return_rect.width) // 2, \
                                                restart_rect.bottom + 50
            screen.blit(return_image, return_rect)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    # 获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    # 如果鼠标在“再来一局”上
                    if restart_rect.left < pos[0] < restart_rect.right and restart_rect.top < pos[
                        1] < restart_rect.bottom:
                        # 调用main函数重新开始游戏
                        pygame.mixer.stop()
                        pygame.mixer.music.stop()
                        main()
                    elif return_rect.left < pos[0] < return_rect.right and return_rect.top < pos[
                        1] < return_rect.bottom:
                        # 退出游戏
                        pygame.quit()
                        sys.exit()

        elif startbutton and not player1.active or not active:
            if gameover_sound_flag :
                gameover_sound_flag = False
                background_sound_flag,win_sound_flag = True,True
                pygame.mixer.init()
                pygame.mixer.music.load(gameover_music_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)

                screen.blit(gameover,gameover_rect)

                # 在屏幕中央绘制'你的分数'
                your_score_text = score_font.render("Your Score: " + str(score), True, (0,0,0))
                your_score_text_rect = your_score_text.get_rect()
                your_score_text_rect.left, your_score_text_rect.top = (width - your_score_text_rect.width) // 2, \
                                                                      height // 4 - your_score_text_rect.height - 40
                screen.blit(your_score_text, your_score_text_rect)

                # 绘制重新开始按钮图标
                again_rect.left, again_rect.top = (width - again_rect.width) // 2, \
                                                  height // 1.5 - 20
                screen.blit(again_image, again_rect)
                # 绘制退出游戏按钮图标
                return_rect.left, return_rect.top = (width - return_rect.width) // 2, \
                                                    again_rect.bottom + 50
                screen.blit(return_image, return_rect)

                # 检测用户的鼠标操作
                # 如果按下左键
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if pygame.mouse.get_pressed()[0]:
                        # 获取鼠标坐标
                        pos = pygame.mouse.get_pos()
                        # 如果鼠标在“重新开始”上
                        if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[
                            1] < again_rect.bottom:
                            # 调用main函数重新开始游戏
                            pygame.mixer.stop()
                            pygame.mixer.music.stop()
                            main()
                        elif return_rect.left < pos[0] < return_rect.right and return_rect.top < pos[
                            1] < return_rect.bottom:
                            # 退出游戏
                            pygame.quit()
                            sys.exit()

        # 更新屏幕
        pygame.display.update()

if __name__ == "__main__":
    try :
        main()
    except SystemExit:
        pass


