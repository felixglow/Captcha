# -*-coding:utf-8 -*-
# 
# Created on 2015-12-29, by felix
# 

__author__ = 'felix'

import os

# 网页验证码
CAPTCHA_FONT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'captcha/fonts/Vera.ttf'))
CAPTCHA_FONT_SIZE = 22
CAPTCHA_IMAGE_SIZE = None
CAPTCHA_PUNCTUATION = '''_"',.;:-'''
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_LETTER_ROTATION = (-35, 35)
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_TIMEOUT = 5
CAPTCHA_LENGTH = 4
CAPTCHA_SOURCE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'