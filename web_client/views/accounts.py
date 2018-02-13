from django.views.generic import CreateView, View, TemplateView
from django.shortcuts import render, redirect, Http404
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from web_client.models import Contractor, Customer
from web_client.forms import ContractorSignUpForm, UpdateContractorForm, CustomerSignUpForm, UpdateCustomerForm


class SignUp(CreateView):
    template_name = 'registration/signup.html'

    # Passes request as parameter to re-use the same method for GET and POST requests.
    def get_form_type(self, request=None):
        if self.kwargs['type'] == 'customer':
            return CustomerSignUpForm(request)
        elif self.kwargs['type'] == 'contractor':
            return ContractorSignUpForm(request)
        else:
            print('Wrong user type:' + self.kwargs['type'])
            raise Http404('Oops, broken URL...')

    def get(self, request, *args, **kwargs):

        form = self.get_form_type()
        return render(request, self.template_name, {'form': form, 'title': 'Create new account'})

    def post(self, request, *args, **kwargs):
        form = self.get_form_type(request.POST)

        if form.is_valid():
            user = form.save()
            login(self.request, user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('welcome')

        return render(request, self.template_name, {'form': form, 'title': 'Create new account'})


@method_decorator([login_required], name='dispatch')
class EditUserDetails(View):
    template_name = 'registration/signup.html'

    def get_form(self, request):
        if request.user.is_contractor:
            return UpdateContractorForm(instance=Contractor.objects.get(user_id=request.user))
        else:
            return UpdateCustomerForm(instance=Customer.objects.get(user_id=request.user))

    def post_form(self, request):
        if request.user.is_contractor:
            return UpdateContractorForm(data=request.POST, instance=Contractor.objects.get(user_id=request.user))
        else:
            return UpdateCustomerForm(data=request.POST, instance=Customer.objects.get(user_id=request.user))

    def get(self, request, *args, **kwargs):
        form = self.get_form(request)
        return render(request, self.template_name, {'form': form, 'title': 'Edit information about your account'})

    def post(self, request, *args, **kwargs):
        form = self.post_form(request)

        if form.is_valid():
            form.save()
            return redirect('homepage')

        return render(request, self.template_name, {'form': form, 'title': 'Edit information about your account'})


@method_decorator([login_required], name='dispatch')
class AccountDetailsModal(TemplateView):
    template_name = 'registration/user_details_modal.html'


@method_decorator([login_required], name='dispatch')
class EditUser(View):
    template_name = 'registration/edit_user.html'

    def get_form(self, request):
        if request.user.is_contractor:
            return UpdateContractorForm(instance=Contractor.objects.get(user_id=request.user))
        else:
            return UpdateCustomerForm(instance=Customer.objects.get(user_id=request.user))

    def post_form(self, request):
        if request.user.is_contractor:
            return UpdateContractorForm(data=request.POST, instance=Contractor.objects.get(user_id=request.user))
        else:
            return UpdateCustomerForm(data=request.POST, instance=Customer.objects.get(user_id=request.user))

    def get(self, request, *args, **kwargs):
        form = self.get_form(request)
        return render(request, self.template_name, {'form': form, 'title': 'Edit information about your account'})

    def post(self, request, *args, **kwargs):
        form = self.post_form(request)
        if form.is_valid():
            form.save()
            success = True
            form = self.get_form(request)
            # return redirect('homepage')
        else:
            success = False

        return render(request, self.template_name, {'success': success, 'form': form, 'title': 'Edit information about your account'})