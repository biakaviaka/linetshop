from models import *

def general(request):
    categories = Category.objects.filter(parent=0, display=1).order_by('ord')
    settings = Settings.objects.all()[0]
    paytype = Paytype.objects.filter(pk=2)[0]

    return {    
                'categories':categories,
                'settings':settings,
                'paytype':paytype,
            }
