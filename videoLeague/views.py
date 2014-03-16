from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from videoLeague.models import videoLeague
from django.conf import settings


@login_required
@user_passes_test(lambda u: u.has_perm('league.can_league'), login_url='/denied')
def index(request):
    v = videoLeague(settings.LEAGUE_PATH)

    if 'voteup' in request.POST:
        v.vote(request.POST['voteup'], request.POST['votedown'])

    ranking = v.get_ranking()

    contestants = v.get_random_contestants()


    return render_to_response('league.html', RequestContext(request, {'video1': contestants[0],
                                                                      'video2': contestants[1],
                                                                      'ranking': ranking[0:10],
                                                                      'deleted': ranking[-5:],
                                                                      'size': len(ranking)
    }))
