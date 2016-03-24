# -*-coding:utf-8 -*-
# 
# Created on 2015-12-29, by felix
#

__author__ = 'felix'

from django.views.generic import View
from django.http.response import JsonResponse

from captcha.models import CaptchaStore
from captcha.generater import captcha_image
from captcha.helpers import captcha_image_url


class Captcha(View):
    """
    验证码显示
    """

    def get(self, request, *args, **kwargs):
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return JsonResponse({"hashkey": hashkey, "image_url": image_url})


class CaptchaImage(View):
    """
    生成验证码图片
    """

    def get(self, request, *args, **kwargs):
        hashkey = kwargs.get('hashkey', '')
        image = captcha_image(hashkey)

        return image

