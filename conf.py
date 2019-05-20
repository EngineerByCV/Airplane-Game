# -*- coding: utf-8 -*-

import sys
import time
import random
import pygame  # 导入动态模块(.dll .pyd .so) 不需要在包名后边跟模块名
import logging
# from Map import Map
# from pygame.locals import *
# from HeroPlane import HeroPlane
# from EnemyPlane import EnemyPlane
# from EnemyPlane2 import EnemyPlane2
# from EnemyPlane3 import EnemyPlane3


# 添加debug日志
LOG_FORMAT = '%(asctime)s %(filename)s %(message)s'
logging.basicConfig(filename='planegame.txt', level=logging.INFO, format=LOG_FORMAT)

# 定义常量(定义后,不再改值)
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512

# 创建敌机列表
enemy_list = []

# # 初始化分数
# score = 0

# 是否重新开始
is_restart = False