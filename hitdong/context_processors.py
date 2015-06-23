# -*- coding: utf-8 -*-
from django.conf import settings


def global_settings(request):
    return {
        'KAKAO_API_KEY': settings.KAKAO_API_KEY
    }
