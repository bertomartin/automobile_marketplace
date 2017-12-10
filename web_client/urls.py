from django.conf.urls import url
from web_client import views

urlpatterns = [
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
]
