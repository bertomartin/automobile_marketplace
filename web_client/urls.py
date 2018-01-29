from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from web_client.views import views, contractor, customer, accounts

urlpatterns = [
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    url(r'^welcome/$', views.WelcomePage.as_view(), name='welcome'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/(?P<type>[\w\-]+)/$', accounts.SignUp.as_view(), name='signup'),
    url(r'^accounts/edit/$', accounts.EditUserDetails.as_view(), name='edit_user'),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # Post management
    url(r'^post/new/$', views.CreatePost.as_view(), name='new_post'),
    url(r'^user/posts/$', views.UserPosts.as_view(), name='user_posts'),
    url(r'^ajax/load-series/$', views.load_series, name='load_series'),
    # url(r'^post/(?P<offer_id>[0-9a-f-]+)$', views.OfferView.as_view(), name='offer'),

    # Vehicle inspection
    url(r'^ajax/inspect/$', views.request_inspection, name='request_inspection'),

]
