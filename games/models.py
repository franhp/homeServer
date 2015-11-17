import os
import random
import re
import shutil
from datetime import datetime
from ffvideo import VideoStream

from django.db import models
from django.db.models import Count
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.conf import settings


class League(models.Model):
    name = models.CharField(max_length=255)
    rules = models.TextField(blank=True)
    library_path = models.CharField(max_length=255, null=True, blank=True)
    play_path = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def ranking(self):
        return Tag.objects.annotate(
            num_videos=Count('taggit_taggeditem_items')
        ).order_by('-num_videos')

    def list_videos(self, videos_path, key=None):
        if videos_path == self.play_path:
            all_videos = list(self.league.filter(
                video_full_path__startswith=self.play_path))
        else:
            all_videos = list(
                self.league.filter(
                    video_full_path__startswith=videos_path
                ).exclude(
                    video_full_path__startswith=self.play_path))

        if key:
            return sorted(all_videos, key=key, reverse=True)
        else:
            return all_videos

    def list_videos_by_popularity(self, videos_path):
        return self.list_videos(videos_path, key=lambda x: x.popularity)

    def list_videos_by_guessed_popularity(self, videos_path):
        return self.list_videos(videos_path, key=lambda x: x.guessed_popularity)

    def list_videos_by_votes(self, videos_path):
        return self.list_videos(videos_path, key=lambda x: x.votes)

    def gather_random_contestants(self, videos_path):
        less_voted_first = self.list_videos(
            videos_path, key=lambda x: x.times_voted)[:20]
        return random.sample(less_voted_first, 2)

    def cleanup(self):
        for video in self.league.all():
            if not os.path.exists(video.video_full_path):
                video.delete()

        def is_commonly_not_used(filename):
            is_directory = os.path.isdir(filename)
            sysfile = filename in ('.DS_Store',)
            return is_directory or sysfile

        def update_video_objects(video_location):

            for root, dirs, files in os.walk(video_location):
                for name in files:
                    video_path = os.path.join(root, name)
                    rel_path = os.path.join(
                        os.path.relpath(root, self.library_path), name)
                    if not is_commonly_not_used(name):
                        v, new = LeagueVideo.objects.get_or_create(
                            video_full_path=video_path,
                            video_rel_path=rel_path,
                            league=self)
                        # if new:
                        #    v.auto_generate_tags()

        update_video_objects(self.library_path)
        update_video_objects(self.play_path)

    def total_size(self, videos_path):
        return sum(x.size for x in self.list_videos(videos_path))


class LeagueVideo(models.Model):
    votes = models.IntegerField(default=0)
    times_voted = models.IntegerField(default=0)
    video_full_path = models.CharField(max_length=255)
    video_rel_path = models.CharField(max_length=255)
    league = models.ForeignKey(League, related_name='league')
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_created=True, default=datetime.now)

    def __unicode__(self):
        return '(%s) %s [%s]' % (self.league, self.name, self.tags)

    @property
    def name(self):
        return os.path.splitext(os.path.basename(self.video_full_path))[0]

    @property
    def popularity(self):
        # if not self.tags.exists():
        #    self.auto_generate_tags()

        score = self.votes
        for tag in self.tags.all():
            score += LeagueVideo.objects.filter(tags=tag).count()
        return score

    @property
    def guessed_popularity(self):
        score = 0
        for word in re.findall(r'[a-zA-Z0-9]+', self.name):
            score += LeagueVideo.objects.filter(tags__name=word.lower()).count()
        return score

    @property
    def duration(self):
        vs = VideoStream(self.video_full_path)
        return '%.2f' % vs.duration  # TODO requires formatting!

    @property
    def poster(self):
        image_filename = self.name + '.jpg'
        image_filepath = os.path.join(settings.THUMBNAILS_DIR, image_filename)
        if not os.path.exists(image_filepath):
            self._generate_thumbnail(image_filepath)
        return image_filename

    def _generate_thumbnail(self, image_filepath):
        vs = VideoStream(self.video_full_path)
        vs.get_frame_at_sec(60).image().save(image_filepath)

    def auto_generate_tags(self):

        def is_too_common(word_part):
            is_video_extension = word_part.upper() in ('THE',)
            is_too_short = len(word_part) <= 3
            is_number = word_part.isdigit()
            return is_video_extension or is_too_short or is_number

        for word in re.findall(r'[a-zA-Z0-9]+', self.name):
            if not is_too_common(word):
                self.tags.add(word.lower())
                self.save()

    @property
    def size(self):
        return os.stat(self.video_full_path).st_size

    def save(self, *args, **kwargs):
        if self.votes < -5:
            self.delete_video()
        else:
            super(LeagueVideo, self).save(*args, **kwargs)

    def vote_down(self):
        self.votes -= 1
        self.times_voted += 1
        self.save()

    def vote_up(self):
        self.votes += 1
        self.times_voted += 1
        self.save()

    def delete_video(self):
        os.remove(self.video_full_path)
        self.delete()

    def archive_video(self):
        dest_filename = os.path.join(
            self.league.library_path,
            os.path.basename(self.video_full_path)
        )
        shutil.move(self.video_full_path, dest_filename)
        self.delete()
