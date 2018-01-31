from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from web_client.views import views, contractor, customer, accounts

urlpatterns = [

    # Homepage
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    url(r'^ajax/load-posts/$', views.Posts.as_view(), name='load_posts'),

    # Authentication/Authorisation
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/(?P<type>[\w\-]+)/$', accounts.SignUp.as_view(), name='signup'),
    url(r'^accounts/edit/$', accounts.EditUserDetails.as_view(), name='edit_user'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^welcome/$', views.WelcomePage.as_view(), name='welcome'),

    # Post management
    url(r'^post/new/$', views.CreatePost.as_view(), name='new_post'),
    url(r'^user/posts/$', views.UserPosts.as_view(), name='user_posts'),
    url(r'^ajax/load-series/$', views.load_series, name='load_series'),
    url(r'^post/(?P<post_id>[0-9a-f-]+)/upload-images/$', views.UploadImages.as_view(), name='upload-images'),

    # Vehicle inspection
    url(r'^ajax/inspect/$', views.request_inspection, name='request_inspection'),
    url(r'^ajax/requests/$', views.InspectionRequests.as_view(), name='get_requests'),

]
