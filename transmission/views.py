from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from transmission.models import transmissionClient


@login_required
@user_passes_test(lambda u: u.has_perm('transmission.can_transmission'), login_url='/denied')
def list(request):
    t = transmissionClient()

    if 'add' in request.POST:
        t.addTorrent(request.POST['add'])

    if 'del' in request.POST:
        t.delTorrent(request.POST['del'])

    return render_to_response('transmission.html', RequestContext(request, {'torrents': t.getTorrents()}))
