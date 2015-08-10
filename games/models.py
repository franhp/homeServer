from collections import Counter
import shutil
import os
import random
import re

from django.db import models


class League(models.Model):
    name = models.CharField(max_length=255)
    rules = models.TextField(blank=True)
    library_path = models.CharField(max_length=255, null=True, blank=True)
    play_path = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def common_words(self):
        def is_too_common(word):
            is_video_extension = word.upper() in ('MP4', 'AVI', 'FLV', 'THE')
            is_too_short = len(word) <= 3
            is_number = word.isdigit()
            return is_video_extension or is_too_short or is_number

        words = []
        for video in self.list_videos(self.library_path):
            for w in video.words:
                if not is_too_common(w):
                    words.append(w.lower())
        return Counter(words)

    def words_ranking(self):
        return reversed(sorted(
            self.common_words().most_common(10), key=lambda x: x[1]))

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

    def list_videos_by_votes(self, videos_path):
        return self.list_videos(videos_path, key=lambda x: x.votes)

    def gather_random_contestants(self, videos_path):
        return random.sample(self.list_videos(videos_path), 2)

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
                        v, _ = LeagueVideo.objects.get_or_create(
                            video_full_path=video_path,
                            video_rel_path=rel_path,
                            league=self)

        update_video_objects(self.library_path)
        # TODO some day they may be separate
        # update_video_objects(self.play_path)

    def total_size(self, videos_path):
        return sum(x.size for x in self.list_videos(videos_path))


class LeagueVideo(models.Model):
    votes = models.IntegerField(default=0)
    video_full_path = models.CharField(max_length=255)
    video_rel_path = models.CharField(max_length=255)
    league = models.ForeignKey(League, related_name='league')

    def __unicode__(self):
        return '(%s) %s' % (self.league, self.name)

    @property
    def name(self):
        return os.path.basename(self.video_full_path)

    @property
    def popularity(self):
        score = 0
        common_words = self.league.common_words()
        for word in self.words:
            for common_word in common_words.items():
                if word == common_word[0]:
                    score += common_word[1]

        return score

    @property
    def words(self):
        return re.findall(r'[a-zA-Z0-9]+', self.name)

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
        self.save()

    def vote_up(self):
        self.votes += 1
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
