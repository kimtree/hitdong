from django.contrib import admin
from hitdong.apps.video.models import Video, VideoAdmin, Tag

admin.site.register(Video, VideoAdmin)
admin.site.register(Tag)
