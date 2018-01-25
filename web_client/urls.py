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

    # Offers management
    url(r'^offer/add/$', views.CreatePost.as_view(), name='new_offer'),
    url(r'^offers/$', views.UserPosts.as_view(), name='user_offers'),
    # url(r'^offer/(?P<offer_id>[0-9a-f-]+)$', views.OfferView.as_view(), name='offer'),

    # Vehicle inspection
    url(r'^ajax/inspect/$', views.request_inspection, name='request_inspection'),
    url(r'^ajax/search/$', views.search, name='search'),

    # url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    # url(r'^search/$', views.Search.as_view(), name='search'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),

]
