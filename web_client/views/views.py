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
    requests_modal = 'homepage/requests_modal.html'
    search_modal = 'homepage/search_modal.html'

    def get(self, request):
        list_of_offers = Post.objects.all()
        search_form = SearchForm()
        if not request.user.is_authenticated:
            contractors = None
            number_of_inspections = None
        else:
            number_of_inspections = len(InspectionRequest.objects.filter(requesting_customer=request.user))
            contractors = Contractor.objects.filter(status=True)

        return render(request, self.template_name, {'offers': list_of_offers,
                                                    'contractors': contractors,
                                                    'search_form': search_form,
                                                    'post_left_modal': self.post_left_modal,
                                                    'post_right_modal': self.post_right_modal,
                                                    'post_representation': self.post_representation,
                                                    'requests_modal': self.requests_modal,
                                                    'search_modal': self.search_modal,
                                                    'view_options': self.view_options,
                                                    'ad_bar': self.ad_bar,
                                                    'number_of_inspections': number_of_inspections})

    def post(self, request):
        form = SearchForm(request.POST)
        query = 'SELECT * FROM web_client_post'
        where_flag = False

        if form.is_valid():
            for field in form.cleaned_data:
                print(field)
                if form.cleaned_data.get(field) is not None:
                    if where_flag is False:
                        query += ' WHERE '
                        where_flag = True
                        query += str(field) + ' = \'' + str(form.cleaned_data.get(field)) + '\''
                    else:
                        query += ' AND ' + str(field) + ' = \'' + str(form.cleaned_data.get(field)) + '\''

        if not request.user.is_authenticated:
            number_of_inspections = None
            contractors = None
        else:
            number_of_inspections = len(InspectionRequest.objects.filter(requesting_customer=request.user))
            contractors = Contractor.objects.filter(status=True)

        list_of_offers = Post.objects.raw(query)
        search_form = SearchForm()

        return render(request, self.template_name, {'offers': list_of_offers,
                                                    'contractors': contractors,
                                                    'search_form': search_form,
                                                    'post_left_modal': self.post_left_modal,
                                                    'post_right_modal': self.post_right_modal,
                                                    'post_representation': self.post_representation,
                                                    'requests_modal': self.requests_modal,
                                                    'search_modal': self.search_modal,
                                                    'view_options': self.view_options,
                                                    'ad_bar': self.ad_bar,
                                                    'number_of_inspections': number_of_inspections})


class Posts(View):
    template_name = 'homepage/post_details.html'

    def get(self, request):
        post_id = request.GET.get('post_id')
        post = Post.objects.get(pk=post_id)
        images = Image.objects.filter(post=post)
        return render(request, self.template_name, {'post': post, 'images': images})

    def post(self, request):
        pass


@method_decorator([login_required], name='dispatch')
class CreatePost(View):
    template_name = 'post/edit_post.html'

    def get(self, request):
        form = OfferForm(initial={'contact_person': Customer.objects.get(user_id=request.user).name})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OfferForm(self.request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('homepage')

        return render(request, self.template_name, {'form': form})


class UploadImages(View):
    template_name = 'post/image_upload.html'

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        images = Image.objects.filter(post_id=post_id)
        return render(self.request, self.template_name, {'photos': images})

    def post(self, request):
        form = ImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


@method_decorator([login_required], name='dispatch')
class UserPosts(View):
    template_name = 'homepage/user_offers.html'

    def get(self, request):
        posts = Post.objects.filter(owner=request.user)
        return render(request, self.template_name, {'offers': posts})

    def post(self, request):
        pass


@method_decorator([login_required], name='dispatch')
class InspectionRequests(View):
    template_name = ''
    inspections = {}

    def get(self, request):
        if request.user.is_customer:
            self.template_name = 'homepage/customer_inspections.html'
            self.inspections = InspectionRequest.objects.filter(requesting_customer=request.user)
        else:
            self.template_name = 'homepage/contractor_inspections.html'
            self.inspections = InspectionRequest.objects.filter(responsible_contractor=Contractor.objects.get(user_id=request.user))

        return render(request, self.template_name, {'inspections': self.inspections})

    def post(self, request):
        pass


def request_inspection(request):
        contractor = Contractor.objects.get(user_id=request.GET.get('contractor_id'))
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
