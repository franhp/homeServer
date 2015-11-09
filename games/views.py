from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import serializers, viewsets
from taggit.models import Tag

from games.models import League, LeagueVideo
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from rest_framework import filters
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class RandomDirectoryCleanerView(TemplateView):
    template_name = 'random_directory_cleaner.html'

    def get(self, request, *args, **kwargs):
        try:
            league = League.objects.get(name='VideoLeague')
            league.cleanup()
        except ObjectDoesNotExist:
            return render(request, self.template_name, {})

        return render(request, self.template_name, {
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


class SearchAndTagView(TemplateView):
    template_name = 'search_and_tag.html'


class ShowVideoView(TemplateView):
    template_name = 'show_video.html'

    def get(self, request, *args, **kwargs):
        try:
            video = LeagueVideo.objects.get(id=self.kwargs.pop('video_id'))
        except ObjectDoesNotExist:
            video = {}

        return render(request, self.template_name, {
            'is_random': video.video_full_path.startswith(
                video.league.play_path),
            'video': video
        })

    def post(self, request, *args, **kwargs):
        vote_up = request.POST.get('vote_up')
        vote_down = request.POST.get('vote_down')
        video_id = kwargs.pop('video_id')

        vid = LeagueVideo.objects.get(id=video_id)
        if vote_up:
            vid.vote_up()
        elif vote_down:
            vid.vote_down()

        return HttpResponseRedirect(reverse('show-video', args=(video_id,)))


class RankingView(TemplateView):
    template_name = 'ranking.html'

    def get_context_data(self, **kwargs):
        context = super(RankingView, self).get_context_data(**kwargs)
        league = League.objects.get(name='VideoLeague')
        context['ranking'] = league.ranking()
        return context


class VideoSerializer(TaggitSerializer, serializers.ModelSerializer):
    name = serializers.CharField()
    league = serializers.CharField(source='league.name')
    tags = TagListSerializerField()
    popularity = serializers.IntegerField()

    class Meta:
        model = LeagueVideo


class VideoView(viewsets.ModelViewSet):
    queryset = LeagueVideo.objects.all()
    serializer_class = VideoSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, )
    search_fields = ('tags__slug', 'tags__name', )
    ordering_fields = '__all__'
    ordering = '-created_at'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

