from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from pyload.models import pyloadClient


@login_required
@user_passes_test(lambda u: u.has_perm('pyload.can_pyload'), login_url='/denied')
def list(request):
    t = pyloadClient()

    if 'add' in request.POST:
        t.addLink(request.POST['add'])

    if 'del' in request.POST:
        t.deleteFinished()

    return render_to_response('pyload.html', RequestContext(request, {'queue': t.getQueue()}))