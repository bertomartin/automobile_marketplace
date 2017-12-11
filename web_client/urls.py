from django.conf.urls import url
from web_client import views

urlpatterns = [
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    url(r'^welcome/$', views.WelcomePage.as_view(), name='welcome'),
    url(r'^signup/$', views.SignUpForm.as_view(), name='signup'),
    # url(r'^signin/$', views.SignInForm.as_view(), name='signin'),

    # url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    # url(r'^search/$', views.Search.as_view(), name='search'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),

]
