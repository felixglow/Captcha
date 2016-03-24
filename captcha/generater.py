# -*-coding:utf-8 -*-
#
# Created on 2015-12-29, by felix
#

import random
import re

from django.conf import settings
from .helpers import noise_arcs, noise_dots, post_smooth
from .models import CaptchaStore
from django.http import HttpResponse, Http404
from PIL import Image, ImageDraw, ImageFont

try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO


NON_DIGITS_RX = re.compile('[^\d]')
# Distance of the drawn text from the top of the captcha image
from_top = 4


def getsize(font, text):
    if hasattr(font, 'getoffset'):
        return [x + y for x, y in zip(font.getsize(text), font.getoffset(text))]
    else:
        return font.getsize(text)


def make_img(size):
    if settings.CAPTCHA_BACKGROUND_COLOR == "transparent":
        image = Image.new('RGBA', size)
    else:
        image = Image.new('RGB', size, settings.CAPTCHA_BACKGROUND_COLOR)
    return image


def captcha_image(hashkey):
    try:
        store = CaptchaStore.objects.get(hashkey=hashkey)
    except CaptchaStore.DoesNotExist:
        return HttpResponse(status=410)

    text = store.challenge
    fontpath = settings.CAPTCHA_FONT_PATH

    if fontpath.lower().strip().endswith('ttf'):
        font = ImageFont.truetype(fontpath, settings.CAPTCHA_FONT_SIZE)
    else:
        font = ImageFont.load(fontpath)

    if settings.CAPTCHA_IMAGE_SIZE:
        size = settings.CAPTCHA_IMAGE_SIZE
    else:
        size = getsize(font, text)
        size = (size[0] * 2, int(size[1] * 1.1))

    image = make_img(size)

    try:
        PIL_VERSION = int(NON_DIGITS_RX.sub('', Image.VERSION))
    except:
        PIL_VERSION = 116
    xpos = 2

    charlist = []
    for char in text:
        if char in settings.CAPTCHA_PUNCTUATION and len(charlist) >= 1:
            charlist[-1] += char
        else:
            charlist.append(char)
    for char in charlist:
        fgimage = Image.new('RGB', size, settings.CAPTCHA_FOREGROUND_COLOR)
        charimage = Image.new('L', getsize(font, ' %s ' % char), '#000000')
        chardraw = ImageDraw.Draw(charimage)
        chardraw.text((0, 0), ' %s ' % char, font=font, fill='#ffffff')
        if settings.CAPTCHA_LETTER_ROTATION:
            if PIL_VERSION >= 116:
                charimage = charimage.rotate(random.randrange(*settings.CAPTCHA_LETTER_ROTATION), expand=0, resample=Image.BICUBIC)
            else:
                charimage = charimage.rotate(random.randrange(*settings.CAPTCHA_LETTER_ROTATION), resample=Image.BICUBIC)
        charimage = charimage.crop(charimage.getbbox())
        maskimage = Image.new('L', size)

        maskimage.paste(charimage, (xpos, from_top, xpos + charimage.size[0], from_top + charimage.size[1]))
        size = maskimage.size
        image = Image.composite(fgimage, image, maskimage)
        xpos = xpos + 2 + charimage.size[0]

    if settings.CAPTCHA_IMAGE_SIZE:
        # centering captcha on the image
        tmpimg = make_img(size)
        tmpimg.paste(image, (int((size[0] - xpos) / 2), int((size[1] - charimage.size[1]) / 2 - from_top)))
        image = tmpimg.crop((0, 0, size[0], size[1]))
    else:
        image = image.crop((0, 0, xpos + 1, size[1]))
    draw = ImageDraw.Draw(image)

    # for f in (noise_arcs, noise_dots):
    #     draw = f(draw, image)
    # image = post_smooth(image)

    for f in (noise_arcs,):
        draw = f(draw, image)
    image = post_smooth(image)

    out = StringIO()
    image.save(out, "PNG")
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    return response


def captcha_refresh(request):

    if not request.is_ajax():
        raise Http404

    new_key = CaptchaStore.generate_key()
    to_json_response = {
        'key': new_key,
        'image_url': captcha_image(new_key),
    }
    return to_json_response
