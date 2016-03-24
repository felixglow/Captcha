# -*-coding:utf-8 -*-
#
# Created on 2015-12-29, by felix
#

__author__ = 'felix'

from django.conf.urls import patterns, url
from .views import Captcha, CaptchaImage

urlpatterns = patterns('',
    url(r'^captcha/$', Captcha.as_view(), name='get_captcha'),
    url(r'^captcha/image/(?P<hashkey>\w+)/$', CaptchaImage.as_view(), name='captcha_image'),
)
