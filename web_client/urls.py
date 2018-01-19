from django.conf.urls import url
from django.contrib.auth import views as auth_views
from web_client.views import views, contractor, customer

urlpatterns = [
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    url(r'^welcome/$', views.WelcomePage.as_view(), name='welcome'),
    # url(r'^signup/$', views.SignUpForm.as_view(), name='signup'),
    url(r'^signup/$', customer.CustomerSignUp.as_view(), name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # Offers management
    url(r'^offer/add/$', views.CreateOffer.as_view(), name='new_offer'),
    url(r'^offers/$', views.UserOffers.as_view(), name='user_offers'),
    url(r'^offer/(?P<offer_id>[0-9a-f-]+)$', views.OfferView.as_view(), name='offer'),

    # Contractors management
    url(r'^contractors/add/$', views.CreateContractor.as_view(), name='add_contractor'),

    # Vehicle inspection
    url(r'^ajax/inspect/$', views.request_inspection, name='request_inspection'),
    url(r'^ajax/search/$', views.autocomplete, name='autocomplete'),

    # url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    # url(r'^search/$', views.Search.as_view(), name='search'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),
    # url(r'^profile/$', views.Profile.as_view(), name='profile'),

]
