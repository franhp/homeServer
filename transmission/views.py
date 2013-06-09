from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from transmission.models import transmissionClient

@login_required
@user_passes_test(lambda u: u.has_perm('home.can_transmission'), login_url='/denied')
def proxy(request):
    t = transmissionClient()
    return render_to_response('transmission.html', RequestContext(request, {'torrents': t.getTorrents()}))
