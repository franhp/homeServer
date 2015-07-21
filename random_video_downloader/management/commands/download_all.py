from django.core.management.base import BaseCommand
from random_video_downloader.models import VideoDownloader, Video

from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Downloads all videos from all websites'

    def handle(self, *args, **options):
        weekly = (datetime.now() - timedelta(days=7))
        for rvd in VideoDownloader.objects.filter(
                scheduled=True, last_execution__lt=weekly):
            print('Queuing %s' % rvd.name)
            rvd.queue_all()

        for vid in Video.objects.filter(status=Video.NOT_STARTED):
            vid.download()
