from django.urls import path

from .views import (index, other_page, BbLoginView, profile, BbLogoutView,
                    ChangeUserInfoView, BbPasswordChangeView)

app_name = 'main'

urlpatterns = [
    path('<str:page>', other_page, name='other'),
    path('', index, name='index'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BbPasswordChangeView.as_view(), name='password_change'),
]
