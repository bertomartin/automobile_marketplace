from django.views.generic import CreateView, UpdateView, View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from web_client.models import ContractorModel
from web_client.forms import ContractorSignUpForm, UpdateContractorForm


class SignUp(CreateView):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = ContractorSignUpForm(None)
        return render(request, self.template_name, {'form': form, 'title': 'Create new account', 'registration': 'Step 1'})

    def post(self, request, *args, **kwargs):
        form = ContractorSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(self.request, user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('edit_contractor')

        return render(request, self.template_name, {'form': form, 'title': 'Create new account', 'registration': 'Step 1'})


class EditUserDetails(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):

        form = UpdateContractorForm(instance=ContractorModel.objects.filter(user_id=request.user).first())
        return render(request, self.template_name, {'form': form, 'title': 'Edit your account', 'registration': 'Step 2'})

    def post(self, request, *args, **kwargs):
        form = UpdateContractorForm(data=request.POST, instance=ContractorModel.objects.filter(user_id=request.user).first())

        if form.is_valid():
            form.save()
            return redirect('welcome')

        return render(request, self.template_name, {'form': form, 'title': 'Edit your account', 'registration': 'Step 2'})
