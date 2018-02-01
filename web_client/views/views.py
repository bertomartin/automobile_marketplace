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
    requests_modal = 'homepage/requests_modal.html'
    search_modal = 'homepage/search_modal.html'

    def get(self, request):
        search_form = SearchForm()
        return render(request, self.template_name, {'search_form': search_form,
                                                    'requests_modal': self.requests_modal,
                                                    'search_modal': self.search_modal
                                                    })

    # TODO move to separate View
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


        list_of_posts = Post.objects.raw(query)
        search_form = SearchForm()

        return render(request, self.template_name, {'search_form': search_form,
                                                    'requests_modal': self.requests_modal,
                                                    'search_modal': self.search_modal
                                                    })


class MainContainer(View):
    template_name = None
    parameters = {}

    def get(self, request):
        if request.user.is_authenticated and request.user.is_contractor:
                self.parameters = {}
                self.template_name = 'homepage/workshop_main_container.html'

        elif request.user.is_authenticated and request.user.is_superuser:
                self.parameters = {}
                self.template_name = 'homepage/admin_main_container.html'
        else:
            self.template_name = 'homepage/customer_main_container.html'
            posts = Post.objects.all().order_by('-created')
            view_options = 'homepage/view_options.html'
            ad_bar = 'homepage/ad_bar.html'
            self.parameters = {'posts': posts,
                               'view_options': view_options,
                               'ad_bar': ad_bar}

        return render(request, self.template_name, self.parameters)


class Posts(View):
    template_name = 'homepage/post_details.html'

    def get(self, request):
        post_id = request.GET.get('post_id')
        post = Post.objects.get(pk=post_id)
        images = Image.objects.filter(post=post)
        return render(request, self.template_name, {'post': post, 'images': images})


class SharingOptions(View):
    template_name = 'homepage/sharing_options.html'

    def get(self, request):
        post_id = request.GET.get('post_id')
        return render(request, self.template_name, {'post_id': Post.objects.get(pk=post_id).pk})


class ContactInformation(View):
    template_name = 'homepage/contact_information_modal.html'

    def get(self, request):
        post_id = request.GET.get('post_id')
        return render(request, self.template_name, {'post': Post.objects.get(pk=post_id)})


class WorkshopsList(View):
    template_name = 'homepage/workshops_modal.html'

    def get(self, request):
        post_id = request.GET.get('post_id')
        user = Customer.objects.get(pk=request.user)
        workshops = Contractor.objects.filter(status=True)
        return render(request, self.template_name, {'user': user, 'post': Post.objects.get(pk=post_id), 'contractors': workshops})


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


@method_decorator([login_required], name='dispatch')
class SeriesPicklist(View):
    template_name = 'post/series_list_options.html'

    def get(self, request):
        manufacturer_id = request.GET.get('manufacturer_id')
        series = Series.objects.filter(make_fk=manufacturer_id).order_by('series')
        return render(request, self.template_name, {'series': series})


@method_decorator([login_required], name='dispatch')
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


def request_inspection(request):

        contractor = Contractor.objects.get(user_id=request.GET.get('contractor_id'))
        post = Post.objects.get(offer_id=request.GET.get('post_id'))
        customer = Customer.objects.get(user=request.user)

        try:
            if InspectionRequest.objects.filter(corresponding_post=post,
                                                responsible_contractor=contractor,
                                                requesting_customer=customer).count() > 0:
                status = 'This request request already exists for this user.'
            else:
                inspection = InspectionRequest(corresponding_post=post,
                                               responsible_contractor=contractor,
                                               requesting_customer=customer)
                inspection.save()
                status = 'Your request to {} was successfully created.'.format(contractor.title)
        except Exception as e:
            status = 'Something went wrong during this request.'
            print('Couldn\'t create inspection request: \n', e)

        return JsonResponse({'status': status})


