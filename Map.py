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


# 创建地图类
class Map(object):
    def __init__(self, img_path, window):
        self.x = 0
        self.bg_img1 = pygame.image.load(img_path)
        self.bg_img2 = pygame.image.load(img_path)
        self.bg1_y = - WINDOW_HEIGHT
        self.bg2_y = 0
        self.window = window

    # 地图移动
    def move(self):
        # 当地图1的 y轴移动到0，则重置
        if self.bg1_y >= 0:
            self.bg1_y = - WINDOW_HEIGHT

        # 当地图2的 y轴移动到 窗口底部，则重置
        if self.bg2_y >= WINDOW_HEIGHT:
            self.bg2_y = 0

        # 每次循环都移动1个像素
        self.bg1_y += 3
        self.bg2_y += 3

    # 地图贴图
    def display(self):
        """贴图"""
        self.window.blit(self.bg_img1, (self.x, self.bg1_y))
        self.window.blit(self.bg_img2, (self.x, self.bg2_y))
