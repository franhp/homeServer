from django.test import TestCase
from games.models import VideoTag, LeagueVideo, League
from django_dynamic_fixture import get


class TestVideoPopularity(TestCase):
    def test_popularity_with_existing_tags(self):
        video1 = get(LeagueVideo)
        tag1 = get(VideoTag, name='tag1', videos=[video1])

        self.assertEqual(tag1.score, 1)
        self.assertEqual(video1.popularity, 1)

    def test_popularity_with_non_existing_tags(self):
        video1 = get(LeagueVideo, video_full_path='/path/to/file.avi')
        self.assertEqual(video1.popularity, 1)
        self.assertEqual(VideoTag.objects.count(), 1)

    def test_popularity_with_higher_scores(self):
        t = get(VideoTag, name='tag1')
        for _ in range(0, 10):
            v = get(LeagueVideo)
            t.videos.add(v)
            t.save()

        self.assertEqual(VideoTag.objects.filter(name='tag1').count(), 1)
        self.assertEqual(LeagueVideo.objects.count(), 10)
        self.assertEqual(LeagueVideo.objects.first().popularity, 10)

    def test_popularity_with_multiple_tags(self):
        v = get(LeagueVideo)
        for num in range(0,10):
            t = get(VideoTag, name='tag' + str(num))
            t.videos.add(v)

        self.assertEqual(v.popularity, 10)

    def test_popularity_contains_votes(self):
        v = get(LeagueVideo, votes=1)
        get(VideoTag, videos=[v])
        self.assertEqual(v.popularity, 2)

    def test_popularity_contains_negative_votes(self):
        v = get(LeagueVideo, votes=-1)
        get(VideoTag, videos=[v])
        self.assertEqual(v.popularity, 0)


class TestLeagues(TestCase):
    def test_ranking(self):
        league = get(League)
        v1 = get(LeagueVideo, league=league)
        v2 = get(LeagueVideo, league=league)
        get(VideoTag, name='tag1', videos=[v1, v2])
        get(VideoTag, name='tag2', videos=[v2])

        ranking = league.ranking()

        self.assertEqual(ranking.first().name, 'tag1')
        self.assertEqual(ranking.first().score, 2)

    def test_get_random_contestants(self):
        league = get(League)
        for times in range(0, 12):
            get(LeagueVideo, times_voted=times, league=league, video_full_path='1')
        league.gather_random_contestants('1')
        # TODO Assert randomness lol



