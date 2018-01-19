from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from web_client.forms import CustomerSignUpForm


class SignUp(CreateView):
    pass
    # template_name = 'registration/signup.html'
    #
    # def get(self, request, *args, **kwargs):
    #     form = CustomerSignUpForm(None)
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = CustomerSignUpForm(request.POST)
    #
    #     if form.is_valid():
    #         user = form.save()
    #         login(self.request, user)
    #
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return redirect('welcome')
    #
    #     return render(request, self.template_name, {'form': form})