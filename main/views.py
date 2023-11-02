from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist


def index(request):
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BbLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')
