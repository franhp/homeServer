from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from rpd.models import RPD
from django.conf import settings
import shutil
import os


@login_required
@user_passes_test(lambda u: u.has_perm('rpd.can_rpd'), login_url='/denied')
def index(request):
    move = delete = ''
    if 'video' in request.POST:
        shutil.move(request.POST['video'], os.path.join('/Users/franhp/code/homeServer', request.POST['short']))
        move = request.POST['short']
    if 'delete' in request.POST:
        os.remove(request.POST['delete'])
        delete = request.POST['short']

    try:
        r = RPD(settings.LIBRARY_PATH, settings.THUMBNAILS_PATH, settings.DOWNLOADS_PATH)
        r.fixFilenames()
        library = r.listVideos()
        counter = r.findMostCommonWords()
        sortedVideos = r.sortVideosByPopularity(library, counter)

    except Exception, err:
        print err
        pass


    return render_to_response('rpd.html', RequestContext(request, {'library': sortedVideos, 'words': counter, 'move': move, 'delete': delete}))