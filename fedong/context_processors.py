# -*- coding: utf-8 -*-
from django.conf import settings
from fedong.functions import get_yesterday


def global_settings(request):
    return {
        'yesterday': get_yesterday(),
        'KAKAO_API_KEY': settings.KAKAO_API_KEY
    }
