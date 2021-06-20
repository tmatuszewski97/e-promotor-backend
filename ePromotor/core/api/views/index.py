from django.http import HttpResponse


# View for basic url


def index(request):
    return HttpResponse("Witaj! Korzystasz z API aplikacji ePromotor")
