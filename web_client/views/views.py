from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from web_client.forms import *
from web_client.models import *


class WelcomePage(TemplateView):
    template_name = 'welcome/welcome.html'


class Homepage(TemplateView):
    template_name = 'homepage/index.html'

    # TODO move to separate View
    # def post(self, request):
    #     form = SearchForm(request.POST)
    #     query = 'SELECT * FROM web_client_post'
    #     where_flag = False
    #
    #     if form.is_valid():
    #         for field in form.cleaned_data:
    #             if form.cleaned_data.get(field) is not None:
    #                 if where_flag is False:
    #                     query += ' WHERE '
    #                     where_flag = True
    #                     query += str(field) + ' = \'' + str(form.cleaned_data.get(field)) + '\''
    #                 else:
    #                     query += ' AND ' + str(field) + ' = \'' + str(form.cleaned_data.get(field)) + '\''
    #
    #
    #     list_of_posts = Post.objects.raw(query)
    #     search_form = SearchForm()
    #
    #     return render(request, self.template_name, {'search_form': search_form,
    #                                                 'requests_modal': self.requests_modal,
    #                                                 'search_modal': self.search_modal
    #                                                 })


class Navbar(View):

    def get_template(self, request):
        if request.user.is_authenticated and request.user.is_contractor:
            return 'navbar/workshop_navbar.html'
        elif request.user.is_authenticated and request.user.is_superuser:
            return 'navbar/admin_navbar.html'
        else:
            return 'navbar/customer_navbar.html'

    def get(self, request):
        template_name = self.get_template(request)
        return render(request, template_name, {})


@method_decorator([login_required], name='dispatch')
class InspectionRequests(View):
    template_name = ''
    inspections = {}

    def get(self, request):
        if request.user.is_customer:
            self.template_name = 'homepage/customer/customer_inspections.html'
            self.inspections = InspectionRequest.objects.filter(requesting_customer=request.user)
        else:
            self.template_name = 'homepage/workshop/contractor_inspections.html'
            self.inspections = InspectionRequest.objects.filter(responsible_contractor=Contractor.objects.get(user_id=request.user))

        return render(request, self.template_name, {'inspections': self.inspections})




