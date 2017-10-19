from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='sign_up'),
    url(r'^member/login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout')
]