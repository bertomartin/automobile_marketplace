from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from web_client.views import views, contractor, customer, accounts

urlpatterns = [

    # Homepage
    url(r'^$', views.Homepage.as_view(), name='homepage'),
    url(r'^ajax/load-main-container/$', views.MainContainer.as_view(), name='load_main_container'),
    url(r'^ajax/load-posts/$', views.Posts.as_view(), name='load_posts'),
    url(r'^ajax/load-post-details/$', views.PostDetails.as_view(), name='load_post_details'),
    url(r'^ajax/load-sharing-options/$', views.SharingOptions.as_view(), name='load_sharing_modal'),
    url(r'^ajax/load-contact-information/$', views.ContactInformation.as_view(), name='load_contact_modal'),
    url(r'^ajax/load-workshops/$', customer.WorkshopsList.as_view(), name='load_workshops_modal'),

    # Workshop's homepage
    url(r'^ajax/load-request-list/$', contractor.RequestList.as_view(), name='load_request_list'),
    url(r'^ajax/load-tab-content/$', contractor.TabContent.as_view(), name='load_tab_content'),

    # Authentication/Authorisation
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/(?P<type>[\w\-]+)/$', accounts.SignUp.as_view(), name='signup'),
    url(r'^accounts/edit/$', accounts.EditUserDetails.as_view(), name='edit_user'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^welcome/$', views.WelcomePage.as_view(), name='welcome'),

    # User preferences
    url(r'^ajax/accounts/user/edit/$', accounts.EditUser.as_view(), name='load_user_modal'),

    # Post management
    url(r'^post/new/$', customer.CreatePost.as_view(), name='new_post'),
    url(r'^user/posts/$', customer.UserPosts.as_view(), name='user_posts'),
    url(r'^ajax/load-series/$', customer.SeriesPicklist.as_view(), name='load_series'),
    url(r'^post/(?P<post_id>[0-9a-f-]+)/upload-images/$', customer.UploadImages.as_view(), name='upload-images'),

    # Vehicle inspection
    url(r'^ajax/request_inspection/$', customer.request_inspection, name='request_inspection'),
    url(r'^ajax/requests/$', views.InspectionRequests.as_view(), name='get_requests'),

]
