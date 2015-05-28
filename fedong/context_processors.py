from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'KAKAO_API_KEY': settings.KAKAO_API_KEY
    }
