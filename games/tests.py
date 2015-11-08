from django.test import TestCase
from taggit.models import Tag

from games.models import LeagueVideo, League

from django_dynamic_fixture import get


class TestVideoPopularity(TestCase):
    def test_popularity_with_existing_tags(self):
        tag1 = get(Tag, name='tag1')
        video1 = get(LeagueVideo, tags=[tag1])


        self.assertEqual(tag1.taggit_taggeditem_items.count(), 1)
        self.assertEqual(video1.popularity, 1)

    def test_popularity_with_non_existing_tags(self):
        video1 = get(LeagueVideo, video_full_path='/path/to/file.avi')
        self.assertEqual(video1.popularity, 1)
        self.assertEqual(Tag.objects.count(), 1)

    def test_popularity_with_higher_scores(self):
        t = get(Tag, name='tag1')
        for _ in range(0, 10):
            v = get(LeagueVideo)
            v.tags.add(t)
            v.save()

        self.assertEqual(Tag.objects.filter(name='tag1').count(), 1)
        self.assertEqual(LeagueVideo.objects.count(), 10)
        self.assertEqual(LeagueVideo.objects.first().popularity, 10)

    def test_popularity_with_multiple_tags(self):
        v = get(LeagueVideo)
        for num in range(0,10):
            t = get(Tag, name='tag' + str(num))
            v.tags.add(t)

        self.assertEqual(v.popularity, 10)

    def test_popularity_contains_votes(self):
        t = get(Tag)
        v = get(LeagueVideo, votes=1, tags=[t])

        self.assertEqual(v.popularity, 2)

    def test_popularity_contains_negative_votes(self):
        t = get(Tag)
        v = get(LeagueVideo, votes=-1, tags=[t])

        self.assertEqual(v.popularity, 0)


class TestLeagues(TestCase):
    def test_ranking(self):
        league = get(League)
        t1 = get(Tag, name='tag1')
        t2 = get(Tag, name='tag2')
        get(LeagueVideo, league=league, tags=[t1])
        get(LeagueVideo, league=league, tags=[t1, t2])

        ranking = league.ranking()

        self.assertEqual(ranking.first().name, 'tag1')
        self.assertEqual(ranking.first().taggit_taggeditem_items.count(), 2)

    def test_get_random_contestants(self):
        league = get(League)
        for times in range(0, 12):
            get(LeagueVideo, times_voted=times, league=league, video_full_path='1')
        league.gather_random_contestants('1')
        # TODO Assert randomness lol



