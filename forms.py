# -*-coding:utf-8 -*-
# 
# Created on 2015-12-29, by felix
# 

__author__ = 'felix'

from django import forms
from django.conf import settings
from .models import CaptchaStore, get_safe_now


class CaptchaForm(forms.Form):
    captcha = forms.CharField(max_length=settings.CAPTCHA_LENGTH, error_messages={
        'required': u'请输入正确的验证码。',
        'max_length': u'请输入正确的验证码。',
    })
    hashkey = forms.CharField(max_length=40, error_messages={
        'required': u'请输入正确的key。',
        'max_length': u'请输入正确的key。',
    })

    def clean(self):
        captcha = self.cleaned_data.get('captcha')
        hashkey = self.cleaned_data.get('hashkey')
        CaptchaStore.remove_expired()

        try:
            CaptchaStore.objects.get(response=captcha, hashkey=hashkey, expiration__gt=get_safe_now()).delete()
        except CaptchaStore.DoesNotExist:
            raise forms.ValidationError(u'验证码错误')