from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic.base import TemplateView
from games.models import League, LeagueVideo
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect


class RandomDirectoryCleanerView(TemplateView):
    template_name = 'random_directory_cleaner.html'
    
    def get(self, request, *args, **kwargs):
        try:
            league = League.objects.get(name='RandomDirectory')
            league.cleanup()
        except ObjectDoesNotExist:
            return render(request, self.template_name, {})

        return render(request, self.template_name, {
            'ranking': league.words_ranking(),
            'videos': league.list_videos_by_popularity(league.play_path),
            'total_size': league.total_size(league.play_path)
        })

    def post(self, request, *args, **kwargs):
        archive = request.POST.get('archive_id')
        delete = request.POST.get('delete_id')
        if archive:
            vid = LeagueVideo.objects.get(id=archive)
            vid.archive_video()
        elif delete:
            vid = LeagueVideo.objects.get(id=delete)
            vid.delete_video()
        return HttpResponseRedirect(reverse('random-directory'))


class LeagueView(TemplateView):
    template_name = 'video_league.html'

    def get(self, request, *args, **kwargs):
        try:
            league = League.objects.get(name='VideoLeague')
            league.cleanup()
            contestants = league.gather_random_contestants(league.library_path)
        except ObjectDoesNotExist:
            return render(request, self.template_name, {})
        return render(request, self.template_name, {
            'ranking': league.list_videos_by_votes(league.library_path),
            'contestant1': contestants[0],
            'contestant2': contestants[1],
            'total_size': league.total_size(league.library_path)
        })

    def post(self, request, *args, **kwargs):
        vote_up = request.POST.get('vote_up')
        vote_down = request.POST.get('vote_down')
        delete_id = request.POST.get('delete_id')

        if vote_up:
            vid1 = LeagueVideo.objects.get(id=vote_up)
            vid1.vote_up()

            vid2 = LeagueVideo.objects.get(id=vote_down)
            vid2.vote_down()

        elif delete_id:
            vid = LeagueVideo.objects.get(id=delete_id)
            vid.delete_video()

        return HttpResponseRedirect(reverse('league'))


class FilterGameView(TemplateView):
    pass
    # TODO IDEA: Tag all the videos, how much time you got?
    # go random playlist!