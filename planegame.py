# -*- coding: utf-8 -*-

import sys
import time
import random
import pygame  # 导入动态模块(.dll .pyd .so) 不需要在包名后边跟模块名
import logging

from EnemyPlane import EnemyPlane
from EnemyPlane2 import EnemyPlane2
from EnemyPlane3 import EnemyPlane3
from HeroBullet import HeroBullet
from Map import Map
from conf import *
from pygame.locals import *

# 添加debug日志
LOG_FORMAT = '%(asctime)s %(filename)s %(message)s'
logging.basicConfig(filename='planegame.txt', level=logging.INFO, format=LOG_FORMAT)

# 初始化分数
score = 0

# # 是否重新开始
# is_restart = False


# 创建英雄类
class HeroPlane(object):
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)  # 图片对象
        self.x = x  # 飞机坐标
        self.y = y
        self.window = window  # 飞机所在的窗口
        self.bullets = []  # 记录该飞机发出的所有子弹
        self.blood = 3
        self.is_anim_down = False
        self.anim_index = 0

    # 判断是否交叉
    def is_hit_enemy(self, enemy):
        if pygame.Rect.colliderect(
            pygame.Rect(self.x, self.y, 120, 78),
            pygame.Rect(enemy.x, enemy.y, 100, 68)
        ):  # 判断是否交叉
            return True
        else:
            return False

    def plane_down_anim(self):
        """敌机被击中动画"""
        if self.anim_index >= 21:  # 动画执行完
            self.blood = 1
            self.is_anim_down = True
            return
        # 敌机血量减1
        self.blood -= 1
        # 显示被击毁的图片
        self.img = pygame.image.load("res/bomb-%d.png" % (self.anim_index // 3 + 1))
        self.anim_index += 1

    def display(self):
        """贴图"""
        # 循环对每个敌机进行判断
        for enemy in enemy_list:
            # 如果与敌机交
            if self.is_hit_enemy(enemy):
                # 英雄血量为0
                self.blood -= 1
                self.plane_down_anim()
                # break

        self.window.blit(self.img, (self.x, self.y))

    def display_bullets(self):
        # 贴子弹图
        deleted_bullets = []

        for bullet in self.bullets:
            # 判断 子弹是否超出 上边界
            if bullet.y >= -31:  # 没有出边界
                bullet.display()
                bullet.move()
            else:  # 飞出边界
                deleted_bullets.append(bullet)

            # 循环判断子弹是否与敌机交叉
            for enemy in enemy_list:
                # 如果交叉
                if bullet.is_hit_enemy(enemy):  # 判断是否击中敌机
                    # 敌机血量减一
                    enemy.blood -= 1
                    # 把该子弹从子弹类表中删除
                    deleted_bullets.append(bullet)
                    # 增加分数
                    global score
                    score += 10
                    break

        for out_window_bullet in deleted_bullets:
            # 删除子弹
            self.bullets.remove(out_window_bullet)

    def move_left(self):
        """往左飞"""
        if self.x >= 0 \
                and self.blood == 1:
            self.x -= 20

    def move_right(self):
        """往右飞"""
        if self.x <= WINDOW_WIDTH - 120 \
                and self.blood == 1:
            self.x += 20

    def move_up(self):
        """往上飞"""
        if self.y >= 0 \
                and self.blood == 1:
            self.y -= 20

    def move_down(self):
        """往下飞"""
        if self.y <= WINDOW_HEIGHT - 78 \
                and self.blood == 1:
            self.y += 20

    def fire(self):
        """发射子弹"""
        # 创建子弹对象  子弹x = 飞机x + 飞机宽度的一半 - 子弹宽度的一半
        count = 0
        # 循环判断子弹位置
        # 如果固定间隔内有子弹就把计数参数加一
        for bullet in self.bullets:
            if self.y - bullet.y <= 120:
                count += 1
        # 如果范围内没有子弹
        if count < 1:
            # 添加子弹实例，发射子弹
            bullet = HeroBullet("res/bullet_%d.png" % random.randint(8, 14), self.x + 60 - 10, self.y - 31, self.window)
            bullet2 = HeroBullet("res/bullet_%d.png" % random.randint(8, 14), self.x + 60 - 40, self.y - 31, self.window)
            bullet3 = HeroBullet("res/bullet_%d.png" % random.randint(8, 14), self.x + 60 + 20, self.y - 31, self.window)
            # 显示子弹(贴子弹图)
            bullet.display()
            bullet2.display()
            bullet3.display()
            self.bullets.append(bullet)  # 为了避免子弹对象被释放(只有局部变量引用对象,方法一执行完就会释放)
            self.bullets.append(bullet2)  # 为了避免子弹对象被释放(只有局部变量引用对象,方法一执行完就会释放)
            self.bullets.append(bullet3)  # 为了避免子弹对象被释放(只有局部变量引用对象,方法一执行完就会释放)


# 创建游戏类
class Game(object):
    def __init__(self):
        pygame.init()
        # 设置标题
        pygame.display.set_caption("飞机大战 v1.0")
        # 设置图标
        game_ico = pygame.image.load("res/app.ico")
        pygame.display.set_icon(game_ico)
        pygame.mixer.music.load("res/bg2.ogg")
        # 游戏结束的音效（超级玛丽）
        self.gameover_sound = pygame.mixer.Sound("res/gameover.wav")
        # 循环播放背景音乐
        pygame.mixer.music.play(-1)
        # 创建窗口  set_mode((窗口尺寸))
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # 创建地图对象
        self.game_map = Map("res/img_bg_level_%d.jpg" % 1, self.window)
        self.game_map2 = Map("res/img_bg_level_%d.jpg" % 2, self.window)
        self.game_map3 = Map("res/img_bg_level_%d.jpg" % 3, self.window)
        # 创建对象
        self.hero_plane = HeroPlane("res/hero{}.png".format(random.randint(1, 2)), 240, 500, self.window)
        for en in range(3):
            self.enemy_plane1 = EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window)
            enemy_list.append(self.enemy_plane1)
        self.enemy_list = enemy_list
        # 创建文字对象
        # self.score_font = pygame.font.SysFont("simhei", 40)
        self.score_font = pygame.font.Font("res/SIMHEI.TTF", 40)

    def draw_text(self, content, size, x, y):
        # font_obj = pygame.font.SysFont("simhei", size)
        font_obj = pygame.font.Font("res/SIMHEI.TTF", size)
        text = font_obj.render(content, 1, (255, 255, 255))
        self.window.blit(text, (x, y))

    def wait_game_input(self):
        # 循环判断事件
        while True:
            # 遍历获取到的事件
            for event in pygame.event.get():
                # 如果是退出键
                if event.type == QUIT:
                    # 退出游戏
                    sys.exit()
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                        pygame.quit()
                    elif event.key == K_RETURN:
                        global is_restart, score
                        is_restart = True
                        score = 0
                        return

    def game_start(self):
        # 贴背景图片
        self.game_map.display()
        self.draw_text("飞机大战", 40, WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 3)
        self.draw_text("按Enter开始游戏, Esc退出游戏.", 28, WINDOW_WIDTH /3 - 140, WINDOW_HEIGHT /2)
        pygame.display.update()
        self.wait_game_input()

    def game_over(self):
        # 先停止背景音乐
        pygame.mixer.music.stop()
        # 再播放音效
        self.gameover_sound.play()
        # 贴背景图片
        self.game_map.display()
        self.draw_text("战机被击落,得分为 %d" % score, 28, WINDOW_WIDTH / 3 - 100, WINDOW_HEIGHT / 3)
        self.draw_text("按Enter重新开始, Esc退出游戏.", 28, WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 2)
        pygame.display.update()
        self.wait_game_input()
        self.gameover_sound.stop()

    def key_control(self):
        # 获取事件，比如按键等  先显示界面,再根据获取的事件,修改界面效果
        for event in pygame.event.get():
            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                sys.exit()  # 让程序终止
                pygame.quit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是空格键
                if event.key == K_SPACE:
                    self.hero_plane.fire()
        # 获取连续按下的情况
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.hero_plane.move_left()

        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.hero_plane.move_right()

        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.hero_plane.move_up()

        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.hero_plane.move_down()

        if pressed_keys[pygame.K_SPACE]:
            self.hero_plane.fire()

    def display1(self):
        # 贴背景图
        self.game_map.display()
        self.game_map.move()
        # 贴飞机图
        self.hero_plane.display()
        self.hero_plane.display_bullets()
        # 贴敌机图
        if len(enemy_list) <= 3:
            enemy_list.append(EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane2("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
        for enemy in enemy_list:
            # 让敌机移动
            if enemy.blood <= 0:
                enemy.display()
                enemy_list.remove(enemy)
                continue
            enemy.display()
            enemy.display_bullets(self.hero_plane)
            enemy.move()

        # 贴得分文字
        score_text = self.score_font.render("得分:%d" % score, 1, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

    def display2(self):
        # 贴背景图
        self.game_map2.display()
        self.game_map2.move()
        # 贴飞机图
        self.hero_plane.display()
        self.hero_plane.display_bullets()
        # 贴敌机图
        if len(enemy_list) <= 6:
            enemy_list.append(EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane2("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
        for enemy in enemy_list:
            # 让敌机移动
            if enemy.blood <= 0:
                enemy.display()
                enemy_list.remove(enemy)
                continue
            enemy.display()
            enemy.display_bullets(self.hero_plane)
            enemy.move()
        # 贴得分文字
        score_text = self.score_font.render("得分:%d" % score, 1, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

    def display3(self):
        # 贴背景图
        self.game_map3.display()
        self.game_map3.move()
        # 贴飞机图
        self.hero_plane.display()
        self.hero_plane.display_bullets()
        # 贴敌机图
        if len(enemy_list) <= 9:
            enemy_list.append(EnemyPlane2("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane2("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
        for enemy in enemy_list:
            # 让敌机移动
            if enemy.blood <= 0:
                enemy.display()
                enemy_list.remove(enemy)
                continue
            enemy.display()
            enemy.display_bullets(self.hero_plane)
            enemy.move()
        # 贴得分文字
        score_text = self.score_font.render("得分:%d" % score, 1, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

    def display4(self):
        # 贴背景图
        self.game_map3.display()
        self.game_map3.move()
        # 贴飞机图
        self.hero_plane.display()
        self.hero_plane.display_bullets()
        # 贴敌机图
        if len(enemy_list) <= 9:
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
        for enemy in enemy_list:
            # 让敌机移动
            if enemy.blood <= 0:
                enemy.display()
                enemy_list.remove(enemy)
                continue
            enemy.display()
            enemy.display_bullets(self.hero_plane)
            enemy.move()
        # 贴得分文字
        score_text = self.score_font.render("得分:%d" % score, 1, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

    def display5(self):
        # 贴背景图
        self.game_map3.display()
        self.game_map3.move()
        # 贴飞机图
        self.hero_plane.display()
        self.hero_plane.display_bullets()
        # 贴敌机图
        if len(enemy_list) <= 9:
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
            enemy_list.append(EnemyPlane3("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100), 0, self.window))
        for enemy in enemy_list:
            # 让敌机移动
            if enemy.blood <= 0:
                enemy.display()
                enemy_list.remove(enemy)
                continue
            enemy.display()
            enemy.display_bullets(self.hero_plane)
            enemy.move()
        # 贴得分文字
        score_text = self.score_font.render("得分:%d" % score, 1, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

    def run(self):
        if is_restart == False:
            self.game_start()
        while True:
            if self.hero_plane.blood <= 0:
                self.hero_plane.blood = 3
                global enemy_list
                enemy_list = []
                break
            # 显示界面
            if score <= 10000:
                self.display1()
            elif score >= 10000:
                self.display2()
            elif score >= 20000:
                self.display3()
            # 键盘控制
            self.key_control()
            # 每次循环,让程序休眠一会儿
            time.sleep(0.01)
        self.game_over()


# 创建主函数
def main():
    """主函数  一般将程序的入口"""
    # 运行游戏
    while True:
        # 创建游戏对象
        game = Game()
        game.run()


if __name__ == '__main__':  # 判断是否主动执行该文件
    main()
