from games.models import League


def leagues(request):
    return {'leagues': League.objects.all()}