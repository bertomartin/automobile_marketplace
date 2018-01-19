from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import JsonResponse
from web_client.forms import CustomerSignUpForm
from web_client.forms import *
from web_client.models import *


class CustomerSignUp(CreateView):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = CustomerSignUpForm(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomerSignUpForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.is_customer = True
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # properly set/change password
            user.set_password(password)
            user.save()
            customer = CustomerModel.objects.create(user=user)

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('welcome')

        return render(request, self.template_name, {'form': form})