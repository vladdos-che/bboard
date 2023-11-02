from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .models import AdvUser
from .forms import ChangeUserInfoForm


def index(request):
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BbLoginView(LoginView):
    template_name = 'main/accounts/login.html'


@login_required
def profile(request):
    return render(request, 'main/accounts/profile.html')


class BbLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/accounts/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/accounts/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'


class BbPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/accounts/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменён'
