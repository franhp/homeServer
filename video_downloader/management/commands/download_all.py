from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from video_downloader.models import VideoDownloader, Video

from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Downloads all videos from all websites'

    def handle(self, *args, **options):
        weekly = (datetime.now() - timedelta(days=7))
        qs = Q(force=True) | (Q(scheduled=True) & Q(last_execution__lt=weekly))
        for rvd in VideoDownloader.objects.filter(qs):
            print('Queuing %s' % rvd.name)
            rvd.queue_all()

        for vid in Video.objects.filter(status=Video.NOT_STARTED):
            vid.download()
