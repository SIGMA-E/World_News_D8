from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import BaseRegisterView


urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('signup/', BaseRegisterView.as_view(), name='signup')
]
