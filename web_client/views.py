from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from web_client.forms import SignUpForm as CreateUser
from web_client.forms import OfferForm
from web_client.models import *


class SignUpForm(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = CreateUser(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateUser(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # properly set/change password
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('welcome')

        return render(request, self.template_name, {'form': form})


class WelcomePage(View):
    template_name = 'welcome/welcome.html'

    def get(self, request):
        return render(request, self.template_name, {'testval': self.template_name})


class Homepage(View):
    template_name = 'homepage/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            login_status = False
            viewing_as = 'Guest'
            list_of_offers = Offer.objects.all()
        else:
            login_status = True
            viewing_as = request.user
            list_of_offers = Offer.objects.all()

        return render(request, self.template_name, {'viewing_as': viewing_as, 'login_status': login_status, 'offers': list_of_offers})


# class CreateOffer(CreateView):
#     template_name = 'offer/offer_form.html'
#     model = Offer
#     fields = ['make', 'model', 'engine', 'body_type']

class CreateOffer(View):
    template_name = 'offer/offer_form.html'
    model = Offer
    fields = ['make', 'model', 'engine', 'body_type']

    def get(self, request):
        form = OfferForm
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


class UserOffers(View):
    template_name = 'user_offers/user_offers.html'

    def get(self, request):
        offers = Offer.objects.filter(owner=request.user)
        return render(request, self.template_name, {'offers': offers})

    def post(self, request):
        pass