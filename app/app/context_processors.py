from django.conf import settings

def constant_text(request):
    return {
        'GOOGLEMAPS_API_KEY': settings.GOOGLEMAPS_API_KEY,
    }