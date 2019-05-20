# -*- coding: utf-8 -*-

import sys
import time
import random
import pygame  # 导入动态模块(.dll .pyd .so) 不需要在包名后边跟模块名
import logging
from conf import *
from pygame.locals import *

# 添加debug日志
from EnemyBullet import EnemyBullet
# from Game import WINDOW_WIDTH, WINDOW_HEIGHT

LOG_FORMAT = '%(asctime)s %(filename)s %(message)s'
logging.basicConfig(filename='planegame.txt', level=logging.INFO, format=LOG_FORMAT)

# # 定义常量(定义后,不再改值)
# WINDOW_HEIGHT = 768
# WINDOW_WIDTH = 512
#
# # 初始化分数
# score = 0
#
# # 是否重新开始
# is_restart = False


# 创建敌机类
class EnemyPlane(object):
    """敌人飞机类"""
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)  # 图片对象
        self.x = x  # 飞机坐标
        self.y = y
        self.window = window  # 飞机所在的窗口
        self.anim_index = 0
        self.hit_sound = pygame.mixer.Sound("res/baozha.ogg")
        self.bullets = []  # 记录该飞机发出的所有子弹
        self.speed = random.randint(1, 3)
        self.blood = 1

    def move(self):
        self.y += self.speed
        # 到达窗口下边界,回到顶部
        if self.y >= WINDOW_HEIGHT:
            self.x = random.randint(0, random.randint(0, WINDOW_WIDTH - 100))
            self.y = 0

    def plane_down_anim(self):
        """敌机被击中动画"""
        if self.anim_index >= 21:  # 动画执行完
            self.anim_index = 0
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))
            self.x = random.randint(0, WINDOW_WIDTH - 100)
            self.y = 0
            self.blood = 1
            return
        elif self.anim_index == 0:
            self.hit_sound.play()
        self.blood -= 1
        self.img = pygame.image.load("res/bomb-%d.png" % (self.anim_index // 3 + 1))
        self.anim_index += 1

    def display(self):
        """贴图"""
        self.fire()
        if self.blood <= 0:
            self.plane_down_anim()

        self.window.blit(self.img, (self.x, self.y))

    def display_bullets(self, hero):
        # 贴子弹图
        deleted_bullets = []

        for bullet in self.bullets:
            # 判断 子弹是否超出 上边界
            if bullet.y >= -31:  # 没有出边界
                bullet.display()
                bullet.move()
            else:  # 飞出边界
                deleted_bullets.append(bullet)

            if bullet.is_hit_enemy(hero):  # 判断是否击中hero
                hero.blood -= 1
                deleted_bullets.append(bullet)
                break

        for out_window_bullet in deleted_bullets:
            self.bullets.remove(out_window_bullet)

    # 判断是否交叉
    def is_hit_enemy(self, enemy):
        if pygame.Rect.colliderect(
                pygame.Rect(self.x, self.y, 120, 78),
                pygame.Rect(enemy.x, enemy.y, 100, 68)
        ):  # 判断是否交叉
            return True
        else:
            return False

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
        if self.y <= random.randint(100, 300):
            count = 0
            for bullet in self.bullets:
                if bullet.y - self.y <= random.randint(300, 500):
                    count += 1
            if count < 1:
                bullet = EnemyBullet("res/bullet_%d.png" % random.randint(1, 7), self.x + 42, self.y + 42, self.window)
                # 显示子弹(贴子弹图)
                bullet.speed = self.speed + random.randint(1, 3)
                bullet.display()
                self.bullets.append(bullet)  # 为了避免子弹对象被释放(只有局部变量引用对象,方法一执行完就会释放)