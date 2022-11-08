from home.models import *


def all_tools(request):
    regions = Region.objects.all()
    prices = Price.objects.all()

    context = {
        'regions': regions,
        'prices': prices
    }
    return context
