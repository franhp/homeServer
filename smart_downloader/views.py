from django import forms
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from smart_downloader.models import Provider, File


class SmartDownloaderView(TemplateView):
    template_name = 'smart_downloader.html'

    def get_context_data(self, **kwargs):
        context = super(SmartDownloaderView, self).get_context_data(**kwargs)
        context['providers'] = Provider.objects.all()
        context['providerless'] = File.objects.filter(
            provider=None, deleted_on=None)
        return context
    
    
    def post(self, request, *args, **kwargs):
        form = SmartDownloaderForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('smart-downloader'))


class SmartDownloaderForm(forms.Form):
    deleted_on = forms.DateTimeField()
    