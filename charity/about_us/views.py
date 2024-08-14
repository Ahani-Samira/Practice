from django.http import HttpResponse
from django.template import loader
from accounts.models import User

def about_us(request):
    charities_list = User.objects.all()
    template = loader.get_template("about_us.html")
    context = {
        "charities_list": charities_list,
    }
    return HttpResponse(template.render(context, request))
