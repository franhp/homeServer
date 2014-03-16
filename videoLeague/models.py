from django.db import models
import os
import random

class Video(models.Model):
    name = models.CharField(max_length=2000)
    video_rel_path = models.CharField(max_length=2000)
    video_full_path = models.CharField(max_length=2000)
    poster = models.CharField(max_length=2000)
    votes = models.IntegerField()
    isdeleted = models.IntegerField()


    def __unicode__(self):
        return self.name

class videoLeague(models.Model): 
    class Meta:
            permissions = (('can_league', 'Can enter the Video League section'),)

    def __init__(self, path):
        self.path = path
        for root, dirs, files in os.walk(self.path):
            for name in files:
                # Detect new videos
                if Video.objects.filter(name=name).count() > 0:
                    print('Video with name [%s] already exists' % name)
                else:
                    print('Creating video with name [%s] ... '%name)
                    v = Video(name=name,
                              video_full_path=os.path.join(root, name),
                              video_rel_path=os.path.join(os.path.relpath(root, path), name),
                              poster=name[:-3] + '50.jpg',
                              isdeleted=0,
                              votes=0)
                    v.save()



    def get_ranking(self):
        return list(Video.objects.filter(isdeleted=0).order_by('-votes'))

    def get_random_contestants(self):
        all_contestants = Video.objects.filter(isdeleted=0)
        return random.sample(all_contestants, 2)


    def vote(self, up, down):
        # One more vote for the winner
        voted_up = Video.objects.get(name=up)
        voted_up.votes = voted_up.votes + 1
        voted_up.save()

        # One vote less for the loser
        voted_down = Video.objects.get(name=down)
        voted_down.votes = voted_down.votes - 1
        voted_down.save()

        # If the loser is is very bad, delete it
        if voted_down.votes < -10:
            os.remove(voted_down.video_full_path)
            voted_down.isdeleted = 1
            voted_down.save()
