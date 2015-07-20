from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from django.shortcuts import render
from django.views.generic.base import View

from models import TransmissionClient


class TransmissionView(View):
    template_name = 'transmission.html'

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {
                'torrents': TransmissionClient.get_torrents()}
        )

    def post(self, request, *args, **kwargs):
        is_delete = request.POST.get('del')
        is_add = request.POST.get('add')
        if is_delete:
            TransmissionClient.del_torrent(is_delete)
        elif is_add:
            TransmissionClient.add_torrent(is_add)
        
        return HttpResponseRedirect(reverse('transmission'))
