from django.conf.urls import url
from web_client import views

urlpatterns = [
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    # url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    # url(r'^search/$', views.Search.as_view(), name='search'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
]
