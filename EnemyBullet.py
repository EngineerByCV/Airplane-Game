# -*- coding: utf-8 -*-

import sys
import time
import random
import pygame  # 导入动态模块(.dll .pyd .so) 不需要在包名后边跟模块名
import logging
from conf import *
from pygame.locals import *

# 添加debug日志
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


# 创建敌机子弹类
class EnemyBullet(object):
    """敌机子弹类"""
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y
        self.window = window
        self.speed = 0
        self.blood = 0

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        """向上飞"""
        self.y += self.speed

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

    def is_hit_enemy(self, hero):
        if pygame.Rect.colliderect(
            pygame.Rect(self.x, self.y, 20, 31),
            pygame.Rect(hero.x, hero.y, 100, 68)
        ):  # 判断是否交叉
            return True
        else:
            return False
