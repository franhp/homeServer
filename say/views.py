import subprocess

from django.shortcuts import render

from django.views.generic.base import TemplateView

from say.models import Sentence


class SayView(TemplateView):
    template_name = 'say.html'

    def post(self, request, *args, **kwargs):
        sentence = request.POST.get('sentence')
        who = request.POST.get('who') or 'Anonymous'

        if sentence:
            Sentence.objects.create(content=sentence, who=who)
            subprocess.Popen(
                '/usr/local/bin/SwitchAudioSource -s "Built-in Output" && osascript -e "set Volume 10" && say "%s says %s" && /usr/local/bin/SwitchAudioSource -s "HDMI"' % (
                    who, sentence),
                shell=True, stdout=subprocess.PIPE)

        return render(request, 'say.html',
                      {'sentences': Sentence.objects.all().order_by('-created_on')})

    def get_context_data(self, **kwargs):
        context = super(SayView, self).get_context_data(**kwargs)
        context['sentences'] = Sentence.objects.all().order_by('-created_on')
        return context
