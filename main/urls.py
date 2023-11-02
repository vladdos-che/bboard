from django.urls import path

from .views import index, other_page, BbLoginView

app_name = 'main'

urlpatterns = [
    path('<str:page>', other_page, name='other'),
    path('', index, name='index'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
]
