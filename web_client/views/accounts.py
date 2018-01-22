from django.views.generic import CreateView, View
from django.shortcuts import render, redirect, Http404
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from web_client.models import Contractor, Customer
from web_client.forms import ContractorSignUpForm, UpdateContractorForm, CustomerSignUpForm, UpdateCustomerForm


class SignUp(CreateView):
    template_name = 'registration/signup.html'

    def get_form_type(self, req):
        if self.kwargs['type'] == 'customer':
            return CustomerSignUpForm(req)
        elif self.kwargs['type'] == 'contractor':
            return ContractorSignUpForm(req)
        else:
            print('Wrong user type:' + self.kwargs['type'])
            raise Http404('Oops, broken URL...')

    def get(self, request, *args, **kwargs):

        form = self.get_form_type(None)
        return render(request, self.template_name, {'form': form, 'title': 'Create new account', 'registration': 'Step 1'})

    def post(self, request, *args, **kwargs):
        form = self.get_form_type(request.POST)

        if form.is_valid():
            user = form.save()
            login(self.request, user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('welcome')

        return render(request, self.template_name, {'form': form, 'title': 'Create new account', 'registration': 'Step 1'})


@method_decorator([login_required], name='dispatch')
class EditUserDetails(View):
    template_name = 'registration/signup.html'

    def get_form(self, request):
        if request.user.is_contractor:
            return UpdateContractorForm(instance=Contractor.objects.filter(user_id=request.user).first())
        else:
            return UpdateCustomerForm(instance=Customer.objects.filter(user_id=request.user).first())

    def post_form(self, request):
        if request.user.is_contractor:
            return UpdateContractorForm(data=request.POST, instance=Contractor.objects.filter(user_id=request.user).first())
        else:
            return UpdateCustomerForm(data=request.POST, instance=Customer.objects.filter(user_id=request.user).first())

    def get(self, request, *args, **kwargs):
        form = self.get_form(request)
        return render(request, self.template_name, {'form': form, 'title': 'We might need some additional information...', 'registration': 'Step 2'})

    def post(self, request, *args, **kwargs):
        form = self.post_form(request)

        if form.is_valid():
            form.save()
            return redirect('homepage')

        return render(request, self.template_name, {'form': form, 'title': 'We might need some additional information...', 'registration': 'Step 2'})
