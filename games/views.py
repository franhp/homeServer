from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic.base import TemplateView
from games.models import League


class RandomDirectoryCleanerView(TemplateView):
    template_name = 'random_directory_cleaner.html'
    
    def get(self, request, *args, **kwargs):
        try:
            league = League.objects.get(name='RandomDirectory')
        except ObjectDoesNotExist:
            return render(request, self.template_name, {})

        return render(request, self.template_name, {
            'ranking': league.words_ranking(),
            'videos': league.list_videos_by_popularity(league.play_path)
        })


class LeagueView(TemplateView):
    template_name = 'video_league.html'

    def get(self, request, *args, **kwargs):
        try:
            league = League.objects.get(name='VideoLeague')
            contestants = league.gather_random_contestants(league.library_path)
        except ObjectDoesNotExist:
            return render(request, self.template_name, {})
        return render(request, self.template_name, {
            'ranking': league.list_videos_by_votes(league.library_path),
            'contestant1': contestants[0],
            'contestant2': contestants[1]
        })
