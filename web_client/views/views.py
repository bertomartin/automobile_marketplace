from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import JsonResponse
from web_client.forms import *
from web_client.models import *


class WelcomePage(View):
    template_name = 'welcome/welcome.html'
    # TODO: different welcome pages for contractors and customers

    def get(self, request):
        return render(request, self.template_name, {'testval': self.template_name})


class Homepage(View):
    template_name = 'homepage/index.html'
    view_options = 'homepage/view_options.html'
    ad_bar = 'homepage/ad_bar.html'
    post_representation = 'homepage/post_details.html'
    post_left_modal = 'homepage/contact_information_modal.html'
    post_right_modal = 'homepage/workshop_list_modal.html'
    list_of_offers = Post.objects.all()

    def get(self, request):
        if not request.user.is_authenticated:
            contractors = None
        else:
            contractors = Contractor.objects.all()

        return render(request, self.template_name, {'offers': self.list_of_offers,
                                                    'contractors': contractors,
                                                    'post_left_modal': self.post_left_modal,
                                                    'post_right_modal': self.post_right_modal,
                                                    'post_representation': self.post_representation,
                                                    'view_options': self.view_options,
                                                    'ad_bar': self.ad_bar})


# class OfferView(View):
#     template_name = ''
#
#     def get_offer(self, offer_id):
#         try:
#             return Post.objects.get(id=offer_id)
#         except:
#             return None
#
#     def get(self, request, offer_id):
#         query_result = self.get_offer(offer_id)
#         return render(request, self.template_name, {'query_result': query_result})


@method_decorator([login_required], name='dispatch')
class CreatePost(View):
    template_name = 'offer/offer_form.html'
    model = Post
    fields = ['make', 'model', 'engine', 'body_type']

    def get(self, request):
        form = OfferForm(initial={'contact_person': request.user.first_name})
        maker_list = Manufacturer.objects.all()
        return render(request, self.template_name, {'form': form, 'maker_list': maker_list})

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
    template_name = 'user_offers/user_offers.html'

    def get(self, request):
        posts = Post.objects.filter(owner=request.user)
        return render(request, self.template_name, {'offers': posts})

    def post(self, request):
        pass


class CreateContractor(View):
    template_name = 'contractor/contractor_form.html'

    def get(self, request):
        form = ContractorForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = form.save(commit=False)
            contractor.save()
            return redirect('homepage')

        return render(request, self.template_name, {'form': form})


def request_inspection(request):
        contractor_id = request.GET.get('contractor_id')
        post_id = request.GET.get('post_id')
        # TODO: add inspection logic
        contractor = Contractor.objects.get(id=contractor_id)
        vehicle = Post.objects.get(offer_id=post_id)
        return JsonResponse({'status': 'ok',
                             'contractor': contractor.title,
                             'vehicle': vehicle.make})


def autocomplete(request):
    search_keyword = request.GET.get('keyword')
    # TODO: get all objects containing 'keyword'
    autocompleter_values = {}
    return JsonResponse(autocompleter_values)
