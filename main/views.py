from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView

from .models import AdvUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


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


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/accounts/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/accounts/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/accounts/bad_signature.html')

    user = get_object_or_404(AdvUser, username=username)

    if user.is_activated:
        templates = 'main/accounts/user_is_activated.html'
    else:
        templates = 'main/accounts/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, templates)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/accounts/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def by_rubric(request, pk):
    pass
