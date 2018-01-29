from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import JsonResponse
from web_client.forms import *
from web_client.models import *


class WelcomePage(View):
    template_name = 'welcome/welcome.html'

    def get(self, request):
        return render(request, self.template_name, {'testval': self.template_name})


class Homepage(View):
    template_name = 'homepage/index.html'
    view_options = 'homepage/view_options.html'
    ad_bar = 'homepage/ad_bar.html'
    post_representation = 'homepage/post_details.html'
    post_left_modal = 'homepage/contact_information_modal.html'
    post_right_modal = 'homepage/workshop_list_modal.html'

    def get(self, request):
        list_of_offers = Post.objects.all()
        search_form = SearchForm()
        if not request.user.is_authenticated:
            contractors = None
        else:
            contractors = Contractor.objects.filter(status=True)

        return render(request, self.template_name, {'offers': list_of_offers,
                                                    'contractors': contractors,
                                                    'search_form': search_form,
                                                    'post_left_modal': self.post_left_modal,
                                                    'post_right_modal': self.post_right_modal,
                                                    'post_representation': self.post_representation,
                                                    'view_options': self.view_options,
                                                    'ad_bar': self.ad_bar})

    def post(self, request):
        form = SearchForm(request.POST)
        query = 'SELECT * FROM web_client_post'
        where_flag = False

        if form.is_valid():
            for field in form.cleaned_data:
                if form.cleaned_data.get(field) is not None:
                    if where_flag is False:
                        query += ' WHERE '
                        where_flag = True
                        query += str(field) + ' = \'' + str(form.cleaned_data.get(field)) + '\''
                    else:
                        query += ' AND ' + str(field) + ' = \'' + str(form.cleaned_data.get(field)) + '\''

        if not request.user.is_authenticated:
            contractors = None
        else:
            contractors = Contractor.objects.filter(status=True)

        list_of_offers = Post.objects.raw(query)
        search_form = SearchForm()

        return render(request, self.template_name, {'offers': list_of_offers,
                                                    'contractors': contractors,
                                                    'search_form': search_form,
                                                    'post_left_modal': self.post_left_modal,
                                                    'post_right_modal': self.post_right_modal,
                                                    'post_representation': self.post_representation,
                                                    'view_options': self.view_options,
                                                    'ad_bar': self.ad_bar})


@method_decorator([login_required], name='dispatch')
class CreatePost(View):
    template_name = 'post/edit_post.html'

    def get(self, request):
        form = OfferForm(initial={'contact_person': Customer.objects.get(user_id=request.user).name})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OfferForm(request.POST)

        if form.is_valid():
            offer = form.save(commit=False)
            offer.owner = request.user
            offer.save()
            return redirect('homepage')

        return render(request, self.template_name, {'form': form})


@method_decorator([login_required], name='dispatch')
class UserPosts(View):
    template_name = 'homepage/user_offers.html'

    def get(self, request):
        posts = Post.objects.filter(owner=request.user)
        return render(request, self.template_name, {'offers': posts})

    def post(self, request):
        pass


def request_inspection(request):
        contractor = User.objects.get(pk=request.GET.get('contractor_id'))
        post = Post.objects.get(offer_id=request.GET.get('post_id'))

        try:
            if len(InspectionRequest.objects.filter(corresponding_post=post,
                                                    responsible_contractor=contractor,
                                                    requesting_customer=request.user)) > 0:
                # print('This request already exists')
                request_created = False
            else:
                inspection = InspectionRequest(corresponding_post=post,
                                               responsible_contractor=contractor,
                                               requesting_customer=request.user)
                inspection.save()
                request_created = True
        except Exception as e:
            request_created = False
            print('Couldn\'t create inspection request: \n', e)

        return JsonResponse({'request_created': request_created,
                             'contractor': Contractor.objects.get(pk=request.GET.get('contractor_id')).title})


def load_series(request):
    manufacturer_id = request.GET.get('manufacturer_id')
    series = Series.objects.filter(make_fk=manufacturer_id).order_by('series')
    return render(request, 'post/series_list_options.html', {'series': series})
