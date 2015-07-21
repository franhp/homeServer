from django.contrib import admin

from random_video_downloader.models import VideoDownloader, Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('provider', 'title', 'status', 'updated_on',)
    search_fields = ('title',)


admin.site.register(VideoDownloader)
admin.site.register(Video, VideoAdmin)
